import json

from ansible.playbook.play import Play as AnsiblePlay
from ansible.playbook.task import Task as AnsibleTask
from ansible.utils.display import Display
from ansible.executor.task_result import TaskResult as AnsibleTaskResult
from ansible.vars.clean import module_response_deepcopy, strip_internal_keys
from ansible.parsing.ajson import AnsibleJSONEncoder


def get_mockable_vars(play: AnsiblePlay) -> dict:
    return {
        k: v
        for k, v in play.get_variable_manager().get_vars().items()
        if k.startswith("mockable_")
    }


def mock_task(task: AnsibleTask, task_mockable_configuration: dict) -> AnsibleTask:
    task.action = "ansible.mockable.plugin"
    task.args = {"return": task_mockable_configuration.get("return", {})}


def get_task_mockable_configuration(
    task: AnsibleTask, mockable_configuration: dict
) -> dict:
    Display().display(f"mockable_configuration = {mockable_configuration}")
    task_mockable_configurations = [
        t
        for t in mockable_configuration.get("tasks", [])
        if (
            (task.get_name() == t.get("name") or t.get("name") is None)
            and (str(task.action) == t.get("plugin") or t.get("plugin") is None)
        )
    ]
    assert len(task_mockable_configurations) <= 1
    task_mockable_configuration = (
        task_mockable_configurations[0] if len(task_mockable_configurations) else {}
    )
    Display().display(f"task_mockable_configuration = {task_mockable_configuration}")

    return task_mockable_configuration


def get_mockable_configuration(mockable_vars: dict) -> dict:
    mockable_scenario = mockable_vars.get("mockable_scenario")
    Display().display(f"mockable_scenario = {mockable_scenario}")
    Display().display(f"mockable_vars = {mockable_vars}")
    mockable_configurations = [
        scenario
        for scenario in mockable_vars.get("mockable_configuration", [])
        if scenario.get("scenario") == mockable_scenario
    ]
    assert len(mockable_configurations) <= 1
    mockable_configuration = (
        mockable_configurations[0] if len(mockable_configurations) else {}
    )
    Display().display(f"mockable_configuration = {mockable_configuration}")
    return mockable_configuration


def get_mockable_filename(mockable_vars: dict) -> str:
    return str(mockable_vars.get("mockable_filename", ""))


def result_to_nice_dict(result: AnsibleTaskResult) -> dict:
    res = {}
    res["plugin"] = str(result._task._action)
    res["name"] = str(result.task_name)
    results = strip_internal_keys(module_response_deepcopy(result._result))

    try:
        jsonified = json.dumps(
            results, cls=AnsibleJSONEncoder, ensure_ascii=False, sort_keys=True
        )
    except TypeError:
        jsonified = json.dumps(
            results, cls=AnsibleJSONEncoder, ensure_ascii=False, sort_keys=False
        )

    results = json.loads(jsonified)
    res["return"] = results
    return res


def get_mockable_scenario(mockable_vars: dict) -> str:
    return str(mockable_vars.get("mockable_scenario", ""))
