# pylint: disable=too-many-lines
"""Provide methods for parsing Ansible artifacts."""

import re
import sys
import uuid
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple, Any, cast, Optional, Union, Callable

import ruamel.yaml as ruamel
from ruamel.yaml.scalarint import BinaryInt, OctalInt, HexInt, HexCapsInt

from detect_secrets.core.secrets_collection import SecretsCollection
from detect_secrets.settings import default_settings
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from spotter.library.parsing.noqa_comments import match_comments_with_task
from spotter.library.scanning.parser_error import YamlErrorDetails
from spotter.library.utils import get_relative_path_to_cwd


class SpotterObfuscated(BaseModel):
    """Class where we save metadata about which fields were obfuscated."""

    type: str
    path: List[Union[int, str]]

    def to_parent(self, path_item: Union[int, str]) -> "SpotterObfuscated":
        """
        Create new object which contains also parent path.

        :param path_item: Path that needs to be inserted at the beginning
        :return: SpotterObfuscated with added parent path
        """
        temp = cast(List[Union[int, str]], [path_item])
        return SpotterObfuscated(type=self.type, path=temp + self.path)


ObfuscatedInput = List[SpotterObfuscated]

# TODO: Rethink if we need to allow parsing and scanning files with other suffixes
YAML_SUFFIXES = (".yml", ".yaml")


class ParsingResult(BaseModel):
    """A container for information about the parsed Ansible artifacts."""

    tasks: List[Dict[str, Any]]
    playbooks: List[Dict[str, Any]]
    dynamic_inventories: List[Dict[str, Any]]
    roles: List[Dict[str, Any]]
    module_defaults: List[Dict[str, Any]]
    errors: List[YamlErrorDetails]

    def tasks_with_relative_path_to_cwd(self) -> List[Dict[str, Any]]:
        """
        Use relative file paths in input tasks.

        :return: Updated tasks with relative paths to cwd
        """
        tasks = self.tasks.copy()
        for t in tasks:
            relative_path = get_relative_path_to_cwd(t["spotter_metadata"]["file"])
            if relative_path:
                t["spotter_metadata"]["file"] = relative_path

        return tasks

    def playbooks_with_relative_path_to_cwd(self) -> List[Dict[str, Any]]:
        """
        Use relative file paths in input playbooks.

        :return: Updated playbooks with relative paths to cwd
        """
        playbooks = self.playbooks.copy()
        for playbook in playbooks:
            for play in playbook["plays"]:
                relative_path = get_relative_path_to_cwd(play["spotter_metadata"]["file"])
                if relative_path:
                    play["spotter_metadata"]["file"] = relative_path

        return playbooks

    def tasks_without_metadata(self) -> List[Dict[str, Any]]:
        """
        Remove sensitive data from input tasks.

        :return: Cleaned list of input tasks
        """
        return [
            {
                "task_id": t["task_id"],
                "play_id": t["play_id"],
                "task_args": t["task_args"],
                "spotter_noqa": t["spotter_noqa"],
            }
            for t in self.tasks
        ]

    def playbooks_without_metadata(self) -> List[Dict[str, Union[str, List[Dict[str, Any]]]]]:
        """
        Remove sensitive data from input playbooks.

        :return: Cleaned list of input playbooks
        """
        return [
            {
                "playbook_id": t["playbook_id"],
                "plays": [{"play_id": x.get("play_id", None), "play_args": x["play_args"]} for x in t["plays"]],
            }
            for t in self.playbooks
        ]

    def clean_inventory(self, include_metadata: bool) -> List[Dict[str, Union[str, List[Dict[str, Any]]]]]:
        if not include_metadata:
            return [
                {
                    "dynamic_inventory_id": i["dynamic_inventory_id"],
                    "dynamic_inventory_args": i["dynamic_inventory_args"],
                }
                for i in self.dynamic_inventories
            ]
        dynamic_inventories = self.dynamic_inventories.copy()
        for i in dynamic_inventories:
            relative_path = get_relative_path_to_cwd(i["spotter_metadata"]["file"])
            if relative_path:
                i["spotter_metadata"]["file"] = relative_path

        return dynamic_inventories


class ScalarBool:
    def __init__(self, bool_value: bool, original_value: str) -> None:
        self.bool_value = bool_value
        self.original_value = original_value

    def __str__(self) -> str:
        return str(self.bool_value)


class ScalarBoolYes(ScalarBool):
    pass


class ScalarBoolNo(ScalarBool):
    pass


class ScalarBoolfactory:
    @staticmethod
    def from_string(value: Any, parsed_value: bool) -> Union[ScalarBool, bool]:
        if value in ["True", "yes", "y", "On", "on"]:
            return ScalarBoolYes(parsed_value, value)
        if value in ["False", "no", "n", "Off", "off"]:
            return ScalarBoolNo(parsed_value, value)
        return parsed_value


class ScalarTimestamp:
    def __init__(self, str_value: str) -> None:
        self.str_value = str_value


class SafeLineConstructor(ruamel.RoundTripConstructor):  # type: ignore
    """YAML loader that adds line numbers."""

    def __init__(self, preserve_quotes: Optional[bool] = None, loader: Any = None) -> None:
        super().__init__(preserve_quotes, loader)
        # add constructors for !vault and !unsafe tags, throw away their values because they are sensitive
        construct_unsafe_or_vault: Callable[[ruamel.SafeLoader, ruamel.Node], Any] = lambda loader, node: None
        self.add_constructor("!unsafe", construct_unsafe_or_vault)
        self.add_constructor("!vault", construct_unsafe_or_vault)
        self.add_constructor("tag:yaml.org,2002:bool", self.construct_yaml_sbool)
        self.add_constructor("tag:ruamel.org,2002:timestamp", ruamel.SafeLoader.construct_yaml_str)

    def construct_yaml_sbool(self, tmp: Any, node: Any = None) -> Any:  # pylint: disable=unused-argument
        value = super().construct_yaml_sbool(node)
        return ScalarBoolfactory.from_string(node.value, value)

    # TODO: Method is not called even if timestamp tag is rewired to us
    def construct_yaml_timestamp(self, node: Any, values: Any = None) -> Any:
        value = super().construct_yaml_str(node)
        return ScalarTimestamp(value)

    def construct_mapping(self, node: ruamel.MappingNode, maptyp: Any, deep: bool = False) -> Dict[Any, Any]:
        """
        Overridden the original construct_mapping method.

        :param node: YAML node object
        :param maptyp: YAML map type
        :param deep: Build objects recursively
        :return: A dict with loaded YAML
        """
        super().construct_mapping(node, maptyp, deep=deep)

        meta = {}
        meta["__line__"] = node.start_mark.line + 1
        meta["__column__"] = node.start_mark.column + 1
        meta["__start_mark_index__"] = node.start_mark.index
        meta["__end_mark_index__"] = node.end_mark.index
        for key in list(maptyp.keys()):
            if isinstance(key, ScalarBool):
                value = maptyp[key]
                del maptyp[key]
                maptyp[key.original_value] = value

        maptyp["__meta__"] = meta
        return maptyp  # type: ignore


class AnsibleArtifact(Enum):
    """Enum that can distinct between different Ansible artifacts (i.e., types of Ansible files)."""

    TASK = 1
    PLAYBOOK = 2
    ROLE = 3
    COLLECTION = 4


class _PlaybookKeywords:
    """
    Enum that stores significant keywords for playbooks that help us automatically discover Ansible file types.

    Keywords were gathered from: https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html.
    """

    PLAY = {
        "any_errors_fatal",
        "become",
        "become_exe",
        "become_flags",
        "become_method",
        "become_user",
        "check_mode",
        "collections",
        "connection",
        "debugger",
        "diff",
        "environment",
        "fact_path",
        "force_handlers",
        "gather_facts",
        "gather_subset",
        "gather_timeout",
        "handlers",
        "hosts",
        "ignore_errors",
        "ignore_unreachable",
        "max_fail_percentage",
        "module_defaults",
        "name",
        "no_log",
        "order",
        "port",
        "post_tasks",
        "pre_tasks",
        "remote_user",
        "roles",
        "run_once",
        "serial",
        "strategy",
        "tags",
        "tasks",
        "throttle",
        "timeout",
        "vars",
        "vars_files",
        "vars_prompt",
    }
    ROLE = {
        "any_errors_fatal",
        "become",
        "become_exe",
        "become_flags",
        "become_method",
        "become_user",
        "check_mode",
        "collections",
        "connection",
        "debugger",
        "delegate_facts",
        "delegate_to",
        "diff",
        "environment",
        "ignore_errors",
        "ignore_unreachable",
        "module_defaults",
        "name",
        "no_log",
        "port",
        "remote_user",
        "run_once",
        "tags",
        "throttle",
        "timeout",
        "vars",
        "when",
    }
    BLOCK = {
        "always",
        "any_errors_fatal",
        "become",
        "become_exe",
        "become_flags",
        "become_method",
        "become_user",
        "block",
        "check_mode",
        "collections",
        "connection",
        "debugger",
        "delegate_facts",
        "delegate_to",
        "diff",
        "environment",
        "ignore_errors",
        "ignore_unreachable",
        "module_defaults",
        "name",
        "no_log",
        "notify",
        "port",
        "remote_user",
        "rescue",
        "run_once",
        "tags",
        "throttle",
        "timeout",
        "vars",
        "when",
    }
    TASK = {
        "action",
        "any_errors_fatal",
        "args",
        "async",
        "become",
        "become_exe",
        "become_flags",
        "become_method",
        "become_user",
        "changed_when",
        "check_mode",
        "collections",
        "connection",
        "debugger",
        "delay",
        "delegate_facts",
        "delegate_to",
        "diff",
        "environment",
        "failed_when",
        "ignore_errors",
        "ignore_unreachable",
        "local_action",
        "loop",
        "loop_control",
        "module_defaults",
        "name",
        "no_log",
        "notify",
        "poll",
        "port",
        "register",
        "remote_user",
        "retries",
        "run_once",
        "tags",
        "throttle",
        "timeout",
        "until",
        "vars",
        "when",
    }


def _load_yaml_file(path: Path) -> Any:
    """
    Load YAML file and return corresponding Python object if parsing has been successful.

    :param path: Path to YAML file
    :return: Parsed YAML file as a Python object
    """
    try:
        yaml_text = path.read_text(encoding="utf-8")
        # remove document start to prevent ruamel changing the YAML version to 1.2
        yaml_text = re.sub(r"^(\s*?)---", r"\1   ", yaml_text, 1)
        yaml = ruamel.YAML(typ="rt")
        yaml.Constructor = SafeLineConstructor
        yaml.version = (1, 1)
        return yaml.load(yaml_text), []
    except ruamel.YAMLError as e:
        if hasattr(e, "problem_mark"):
            return None, [
                YamlErrorDetails(
                    column=e.problem_mark.column,
                    index=e.problem_mark.index,
                    line=e.problem_mark.line + 1,
                    description=e.problem,
                    file_path=path,
                )
            ]
        print(f"Something went wrong when parsing:\n{path.name}: {e}", file=sys.stderr)
        return None, []
    except UnicodeDecodeError as e:
        print(f"{path.name}: {e}", file=sys.stderr)
        return None, []


def _is_playbook(loaded_yaml: Any) -> bool:
    """
    Check if file is a playbook = a YAML file containing one or more plays in a list.

    :param loaded_yaml: Parsed YAML file as a Python object
    :return: True or False
    """
    # use only keywords that are unique for play and do not intersect with other keywords
    playbook_keywords = _PlaybookKeywords.PLAY.difference(
        _PlaybookKeywords.TASK.union(_PlaybookKeywords.BLOCK).union(_PlaybookKeywords.ROLE)
    )

    if isinstance(loaded_yaml, list):
        if any(len(playbook_keywords.intersection(e.keys())) > 0 for e in loaded_yaml if isinstance(e, dict)):
            return True

    return False


def _is_dynamic_inventory(loaded_yaml: Any) -> bool:
    """
    Check if file is a dynamic inventory definition.

    :param loaded_yaml: Parsed YAML file as a Python object
    :return: True or False
    """
    if not isinstance(loaded_yaml, dict):
        return False
    if not "plugin" in loaded_yaml:
        return False
    return True


def _is_role(directory: Path) -> bool:
    """
    Check if directory is a role = a directory with at least one of eight main standard directories.

    :param directory: Path to directory
    :return: True or False
    """
    standard_role_directories = ["tasks", "handlers", "library", "defaults", "vars", "files", "templates", "meta"]

    if any((directory / d).exists() for d in standard_role_directories):
        return True
    return False


def _is_collection(directory: Path) -> bool:
    """
    Check if directory is a collection = a directory with galaxy.yml or roles or plugins.

    :param directory: Path to directory
    :return: True or False
    """
    if (directory / "galaxy.yml").exists() or (directory / "roles").exists() or (directory / "plugins").exists():
        return True
    return False


def _clean_action_and_local_action(task: Dict[str, Any], parse_values: bool = False) -> None:
    """
    Handle parsing Ansible task that include action or local_action keys.

    This is needed because tasks from action or local_action have different syntax and need to be cleaned to look the
    same as other tasks.

    :param task: Ansible task
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Cleaned Ansible task
    """
    # TODO: Remove this spaghetti when API will be able to parse action plugins
    if parse_values:
        # server handles that case already
        return

    if not isinstance(task, dict):
        # probably inlined - we do not cover that case without parsed values
        return

    if not ("action" in task or "local_action" in task):
        # nothing to do
        return

    # replace action or local_action with the name of the module they contain and set delegate_to for local_action
    verb = "action" if "action" in task else "local_action"
    dict_with_module = next((d for d in list(task.values()) if isinstance(d, dict) and "module" in d), None)
    if dict_with_module is not None:
        module_name = dict_with_module.pop("module", None)
        action = task.pop(verb, None)
        task[module_name] = action
        if verb == "local_action":
            task["delegate_to"] = None


def _remove_deep_metadata(task: Any) -> Any:
    """
    Remove nested metadata.

    :param task: Ansible task
    :return: Updated Ansible task
    """
    if not task:
        return task

    if isinstance(task, dict):
        return {k: _remove_deep_metadata(v) for k, v in task.items() if k != "__meta__"}

    if isinstance(task, list):
        return [_remove_deep_metadata(x) for x in task]

    return task


def _remove_parameter_values(task: Dict[str, Any], params_to_keep: Optional[List[str]] = None) -> None:
    """
    Remove parameter values from Ansible tasks.

    :param task: Ansible task
    :param params_to_keep: List of parameters that should not be removed
    """
    for task_key in task:
        if isinstance(task[task_key], dict):
            for key in list(task[task_key]):
                if task_key in ["action", "local_action"] and key == "module":
                    continue
                if key != "__meta__":
                    task[task_key][key] = None
        else:
            if not params_to_keep or task_key not in params_to_keep:
                task[task_key] = None


def detect_secrets_in_file(file_name: str) -> List[str]:
    """
    Detect secret parameter values (e.g., passwords, SSH keys, API tokens, cloud credentials, etc.) in the file.

    :param file_name: Name of the original file with tasks
    :return: List of secrets as strings
    """
    secret_values = []
    secrets_collection = SecretsCollection()
    with default_settings():
        secrets_collection.scan_file(file_name)
        for secret_set in secrets_collection.data.values():
            for secret in secret_set:
                if secret.secret_value:
                    secret_values.append(secret.secret_value)

    return secret_values


def _remove_secret_parameter_from_dict(yaml_key: Dict[str, Any], secrets: List[str]) -> Tuple[Any, ObfuscatedInput]:
    obfuscated: ObfuscatedInput = []
    result = {}
    for key, value in yaml_key.items():
        cleaned, items = _remove_secret_parameter_values(value, secrets)
        result[key] = cleaned
        obfuscated.extend(item.to_parent(key) for item in items)
    return result, obfuscated


def _remove_secret_parameter_from_list(yaml_key: List[Any], secrets: List[str]) -> Tuple[Any, ObfuscatedInput]:
    obfuscated: ObfuscatedInput = []
    result = []
    for key, value in enumerate(yaml_key):
        cleaned, items = _remove_secret_parameter_values(value, secrets)
        result.append(cleaned)
        obfuscated.extend(item.to_parent(key) for item in items)
    return result, obfuscated


def _remove_secret_parameter_values(yaml_key: Any, secret_values: List[str]) -> Tuple[Any, ObfuscatedInput]:
    """
    Remove secret parameter values from YAML.

    :param yaml_key: YAML key
    :param secret_values: List of detected secret values
    :return: Updated YAML key
    """
    # pylint: disable=too-many-return-statements
    if isinstance(yaml_key, dict):
        return _remove_secret_parameter_from_dict(yaml_key, secret_values)

    if isinstance(yaml_key, list):
        return _remove_secret_parameter_from_list(yaml_key, secret_values)

    if isinstance(yaml_key, str) and any(secret_value in yaml_key for secret_value in secret_values):
        return None, [SpotterObfuscated(type="str", path=[])]

    if isinstance(yaml_key, BinaryInt):
        return yaml_key, [SpotterObfuscated(type="BinaryInt", path=[])]
    if isinstance(yaml_key, OctalInt):
        return yaml_key, [SpotterObfuscated(type="OctalInt", path=[])]
    if isinstance(yaml_key, HexInt):
        return yaml_key, [SpotterObfuscated(type="HexInt", path=[])]
    if isinstance(yaml_key, HexCapsInt):
        return yaml_key, [SpotterObfuscated(type="HexCapsInt", path=[])]

    if isinstance(yaml_key, ScalarTimestamp):
        return yaml_key.str_value, [SpotterObfuscated(type="Timestamp", path=[])]

    if isinstance(yaml_key, ScalarBool):
        return yaml_key.bool_value, [SpotterObfuscated(type=yaml_key.__class__.__name__, path=[])]

    return yaml_key, []


# pylint: disable=too-many-locals
def _parse_tasks(
    tasks: List[Dict[str, Any]], file_name: str, parse_values: bool = False, play_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Parse Ansible tasks and prepare them for scanning.

    :param tasks: List of Ansible task dicts
    :param file_name: Name of the original file with tasks
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :param play_id: Unique identifier for play that tasks belong to
    :return: List of parsed Ansible tasks
    """
    try:
        parsed_tasks = []
        secrets = detect_secrets_in_file(file_name)

        for task in [t for t in tasks if t is not None]:
            contains_block_section = False
            for block_section in ("block", "rescue", "always"):
                if block_section in task:
                    contains_block_section = True
                    if isinstance(task[block_section], list):
                        parsed_tasks += _parse_tasks(task[block_section], file_name, parse_values)
            if contains_block_section:
                continue

            if isinstance(task, ruamel.CommentedMap):
                match_comments_with_task(task)

            task_copy: Dict[str, Any] = dict(task)
            task_meta = task_copy.pop("__meta__", None)
            task_noqa = task_copy.pop("__noqa__", [])
            obfuscated: ObfuscatedInput = []

            if not parse_values:
                _remove_parameter_values(task_copy)
            else:
                for task_key in task_copy:
                    task_copy[task_key], hidden = _remove_secret_parameter_values(task_copy[task_key], secrets)
                    obfuscated.extend(item.to_parent(task_key) for item in hidden)

            meta = {
                "file": file_name,
                "line": task_meta["__line__"],
                "column": task_meta["__column__"],
                "start_mark_index": task_meta["__start_mark_index__"],
                "end_mark_index": task_meta["__end_mark_index__"],
            }

            task_dict = {
                "task_id": str(uuid.uuid4()),
                "play_id": play_id,
                "task_args": _remove_deep_metadata(task_copy),
                "spotter_metadata": meta,
                "spotter_obfuscated": [to_jsonable_python(x) for x in obfuscated],
                "spotter_noqa": [to_jsonable_python(x) for x in task_noqa],
            }
            parsed_tasks.append(task_dict)

        return parsed_tasks
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error: parsing tasks from {file_name} failed: {e}", file=sys.stderr)
        return []


def _parse_dynamic_inventory(
    dynamic_inventory: Dict[str, Any], file_name: str, parse_values: bool = False
) -> Dict[str, Any]:
    secrets = detect_secrets_in_file(file_name)

    if isinstance(dynamic_inventory, ruamel.CommentedMap):
        match_comments_with_task(dynamic_inventory)

    dynamic_inventory_copy: Dict[str, Any] = dict(dynamic_inventory)
    dynamic_inventory_meta = dynamic_inventory_copy.pop("__meta__", None)
    dynamic_inventory_noqa = dynamic_inventory_copy.pop("__noqa__", [])
    obfuscated: ObfuscatedInput = []

    if not parse_values:
        _remove_parameter_values(dynamic_inventory_copy, ["plugin", "plugin_type"])
    else:
        for key in dynamic_inventory_copy:
            dynamic_inventory_copy[key], hidden = _remove_secret_parameter_values(dynamic_inventory_copy[key], secrets)
            obfuscated.extend(item.to_parent(key) for item in hidden)

    meta = {
        "file": file_name,
        "line": dynamic_inventory_meta["__line__"],
        "column": dynamic_inventory_meta["__column__"],
        "start_mark_index": dynamic_inventory_meta["__start_mark_index__"],
        "end_mark_index": dynamic_inventory_meta["__end_mark_index__"],
    }
    parsed_dynamic_inventory = {
        "dynamic_inventory_id": str(uuid.uuid4()),
        "dynamic_inventory_args": _remove_deep_metadata(dynamic_inventory_copy),
        "spotter_metadata": meta,
        "spotter_obfuscated": [to_jsonable_python(x) for x in obfuscated],
        "spotter_noqa": [to_jsonable_python(x) for x in dynamic_inventory_noqa],
    }
    return parsed_dynamic_inventory


def _parse_play(
    play: Dict[str, Any], file_name: str, parse_values: bool = False, play_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parse Ansible play and prepare it for scanning.

    :param play: Ansible play dict
    :param file_name: Name of the original file with play
    :param parse_values: True if also read values (apart from parameter names) from play parameters, False if not
    :param play_id: Unique identifier for this play
    :return: Dict with parsed Ansible play
    """
    try:
        play_meta = play.pop("__meta__", None)

        obfuscated: ObfuscatedInput = []
        if not parse_values:
            _remove_parameter_values(play, ["collections"])
        else:
            secrets = detect_secrets_in_file(file_name)
            for play_key in play:
                play[play_key], hidden = _remove_secret_parameter_values(play[play_key], secrets)
                obfuscated.extend(item.to_parent(play_key) for item in hidden)

        meta = {
            "file": file_name,
            "line": play_meta["__line__"],
            "column": play_meta["__column__"],
            "start_mark_index": play_meta["__start_mark_index__"],
            "end_mark_index": play_meta["__end_mark_index__"],
        }

        play_dict = {
            "play_id": play_id,
            "play_args": _remove_deep_metadata(play),
            "spotter_metadata": meta,
            "spotter_obfuscated": [to_jsonable_python(x) for x in obfuscated],
        }

        return play_dict
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error: parsing play from {file_name} failed: {e}", file=sys.stderr)
        return {}


def _parse_playbook(
    playbook: List[Dict[str, Any]], file_name: str, parse_values: bool = False
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Parse Ansible playbook and prepare it for scanning.

    :param playbook: Ansible playbook as dict
    :param file_name: Name of the original file with playbook
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_tasks = []
    parsed_plays = []
    for play in [p for p in playbook if p is not None]:
        tasks = play.pop("tasks", [])
        pre_tasks = play.pop("pre_tasks", [])
        post_tasks = play.pop("post_tasks", [])
        handlers = play.pop("handlers", [])

        all_tasks = ruamel.CommentedSeq()
        if isinstance(tasks, list):
            all_tasks.extend(tasks)
        if isinstance(pre_tasks, list):
            all_tasks.extend(pre_tasks)
        if isinstance(post_tasks, list):
            all_tasks.extend(post_tasks)
        if isinstance(handlers, list):
            all_tasks.extend(handlers)

        play_id = str(uuid.uuid4())
        parsed_tasks += _parse_tasks(all_tasks, file_name, parse_values, play_id)
        parsed_plays.append(_parse_play(play, file_name, parse_values, play_id))

    parsed_playbook = {"playbook_id": str(uuid.uuid4()), "plays": parsed_plays}
    return parsed_tasks, [parsed_playbook]


def _parse_role(
    directory: Path, parse_values: bool = False
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], List[YamlErrorDetails]]:
    """
    Parse Ansible role.

    :param directory: Role directory
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_role_tasks = []
    parsed_errors = []
    for task_file in sorted(list((directory / "tasks").rglob("*")) + list((directory / "handlers").rglob("*"))):
        if task_file.is_file() and task_file.suffix in YAML_SUFFIXES:
            loaded_yaml, yaml_errors = _load_yaml_file(task_file)
            if yaml_errors:
                parsed_errors += yaml_errors
            if isinstance(loaded_yaml, list):
                parsed_role_tasks += _parse_tasks(loaded_yaml, str(task_file), parse_values)

    # read role specification
    arg_spec_file = directory / "meta" / "argument_specs.yml"
    try:
        parsed_role_args_spec, role_spec_errors = _load_yaml_file(arg_spec_file)
        parsed_errors += role_spec_errors
    except FileNotFoundError:
        parsed_role_args_spec = None

    parsed_role = {
        "role_id": str(uuid.uuid4()),
        "role_name": directory.stem,
        "role_argument_specification": _remove_deep_metadata(parsed_role_args_spec) if parsed_role_args_spec else None,
        "spotter_metadata": {
            "column": 0,
            "end_mark_index": 0,
            "file": str(directory),
            "line": 0,
            "start_mark_index": 0,
        },
    }
    return parsed_role_tasks, [], parsed_role, parsed_errors


def _parse_collection(
    directory: Path, parse_values: bool = False
) -> Tuple[
    List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[YamlErrorDetails]
]:
    """
    Parse Ansible collection.

    :param directory: Collection directory
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_collection_tasks = []
    parsed_collection_playbooks = []
    parsed_dynamic_inventories = []
    parsed_collection_roles = []
    parsed_errors = []
    for role in sorted(list((directory / "roles").rglob("*"))):
        if role.is_dir():
            parsed_tasks, _, parsed_role, yaml_errors = _parse_role(role, parse_values)
            parsed_collection_tasks += parsed_tasks
            if role.parent.name == "roles":
                parsed_collection_roles += [parsed_role]
            parsed_errors += yaml_errors
    for playbook in sorted(list((directory / "playbooks").rglob("*"))):
        if playbook.is_file() and playbook.suffix in YAML_SUFFIXES:
            loaded_yaml, yaml_errors = _load_yaml_file(playbook)
            if _is_playbook(loaded_yaml):
                parsed_tasks, parsed_playbooks = _parse_playbook(loaded_yaml, str(playbook), parse_values)
                parsed_collection_tasks += parsed_tasks
                parsed_collection_playbooks += parsed_playbooks
    for role in sorted(list((directory / "tests" / "integration" / "targets").glob("*"))):
        parsed_tasks, parsed_playbooks, parsed_role, yaml_errors = _parse_role(role, parse_values)
        parsed_collection_tasks += parsed_tasks
        parsed_collection_playbooks += parsed_playbooks
        parsed_collection_roles += [parsed_role]
        parsed_errors += yaml_errors
    for path in sorted(list(directory.glob("*.yml")) + list(directory.glob("*.yaml"))):
        if path.is_file() and path.suffix in YAML_SUFFIXES:
            loaded_yaml, yaml_errors = _load_yaml_file(path)
            parsed_errors += yaml_errors
            if _is_playbook(loaded_yaml):
                parsed_tasks, parsed_playbooks = _parse_playbook(loaded_yaml, str(path), parse_values)
                parsed_collection_tasks += parsed_tasks
                parsed_collection_playbooks += parsed_playbooks
            elif _is_dynamic_inventory(loaded_yaml):
                parsed_dynamic_inventory = _parse_dynamic_inventory(loaded_yaml, str(path), parse_values)
                parsed_dynamic_inventories += [parsed_dynamic_inventory]
            elif isinstance(loaded_yaml, list):
                parsed_collection_tasks += _parse_tasks(loaded_yaml, str(path), parse_values)
    return (
        parsed_collection_tasks,
        parsed_collection_playbooks,
        parsed_dynamic_inventories,
        parsed_collection_roles,
        parsed_errors,
    )


def parse_unknown_ansible_artifact(
    path: Path, parse_values: bool = False
) -> Tuple[
    List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[YamlErrorDetails]
]:
    """
    Parse Ansible artifact (unknown by type) by applying automatic Ansible file type detection.

    We are able to can discover task files, playbooks, roles and collections at any level recursively.

    :param path: Path to file or directory
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: Tuple containing list of parsed Ansible tasks and parsed playbook as dict
    """
    parsed_ansible_artifacts_tasks = []
    parsed_ansible_artifacts_playbooks = []
    parsed_ansible_artifacts_dynamic_inventories = []
    parsed_ansible_artifacts_roles = []

    parsed_errors = []

    if path.is_file() and path.suffix in YAML_SUFFIXES:
        loaded_yaml, yaml_error = _load_yaml_file(path)
        if yaml_error is not None:
            parsed_errors += yaml_error
        if _is_playbook(loaded_yaml):
            parsed_tasks, parsed_playbooks = _parse_playbook(loaded_yaml, str(path), parse_values)
            parsed_ansible_artifacts_tasks += parsed_tasks
            parsed_ansible_artifacts_playbooks += parsed_playbooks
        elif _is_dynamic_inventory(loaded_yaml):
            parsed_ansible_artifacts_dynamic_inventories += [
                _parse_dynamic_inventory(loaded_yaml, str(path), parse_values)
            ]
        elif isinstance(loaded_yaml, list):
            parsed_ansible_artifacts_tasks += _parse_tasks(loaded_yaml, str(path), parse_values)
    if path.is_dir():
        if _is_collection(path):
            # TODO: parse inventory files
            parsed_tasks, parsed_playbooks, parsed_dynamic_inventories, parsed_roles, yaml_error = _parse_collection(
                path, parse_values
            )
            parsed_ansible_artifacts_tasks += parsed_tasks
            parsed_ansible_artifacts_playbooks += parsed_playbooks
            parsed_ansible_artifacts_dynamic_inventories += parsed_dynamic_inventories
            parsed_ansible_artifacts_roles += parsed_roles
            parsed_errors += yaml_error
        elif _is_role(path):
            parsed_tasks, parsed_playbooks, parsed_role, yaml_error = _parse_role(path, parse_values)
            parsed_ansible_artifacts_tasks += parsed_tasks
            parsed_ansible_artifacts_playbooks += parsed_playbooks
            parsed_ansible_artifacts_roles += [parsed_role]
            parsed_errors += yaml_error
        else:
            for sub_path in sorted(path.iterdir()):
                (
                    parsed_tasks,
                    parsed_playbooks,
                    parsed_dynamic_invenroties,
                    parsed_ansible_roles,
                    yaml_error,
                ) = parse_unknown_ansible_artifact(sub_path, parse_values)
                parsed_ansible_artifacts_tasks += parsed_tasks
                parsed_ansible_artifacts_playbooks += parsed_playbooks
                parsed_ansible_artifacts_dynamic_inventories += parsed_dynamic_invenroties
                parsed_ansible_roles += parsed_ansible_artifacts_roles
                parsed_errors += yaml_error

    return (
        parsed_ansible_artifacts_tasks,
        parsed_ansible_artifacts_playbooks,
        parsed_ansible_artifacts_dynamic_inventories,
        parsed_ansible_artifacts_roles,
        parsed_errors,
    )


def parse_ansible_artifacts(paths: List[Path], parse_values: bool = False) -> ParsingResult:
    """
    Parse multiple Ansible artifacts.

    :param paths: List of paths to Ansible artifacts
    :param parse_values: True if also read values (apart from parameter names) from task parameters, False if not
    :return: ParsingResult object with list of parsed Ansible tasks and playbooks that are prepared for scanning
    """
    parsed_ansible_artifacts_tasks = []
    parsed_ansible_artifacts_playbooks = []
    parsed_ansible_artifacts_dynamic_inventories = []
    parsed_ansible_artifacts_roles = []
    parsed_errors = []
    for path in paths:
        (
            parsed_tasks,
            parsed_playbooks,
            parsed_dynamic_inventories,
            parsed_roles,
            yaml_error,
        ) = parse_unknown_ansible_artifact(path, parse_values)
        parsed_ansible_artifacts_tasks += parsed_tasks
        parsed_ansible_artifacts_playbooks += parsed_playbooks
        parsed_ansible_artifacts_dynamic_inventories += parsed_dynamic_inventories
        parsed_ansible_artifacts_roles += parsed_roles
        parsed_errors += yaml_error

    return ParsingResult(
        tasks=parsed_ansible_artifacts_tasks,
        playbooks=parsed_ansible_artifacts_playbooks,
        dynamic_inventories=parsed_ansible_artifacts_dynamic_inventories,
        roles=parsed_ansible_artifacts_roles,
        module_defaults=[],
        errors=parsed_errors,
    )
