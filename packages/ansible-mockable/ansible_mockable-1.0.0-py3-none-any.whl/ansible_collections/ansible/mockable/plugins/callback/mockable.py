from __future__ import absolute_import, division, print_function

import yaml

__metaclass__ = type
from ansible.plugins.callback import CallbackBase
from ansible.utils.display import Display
from ansible.executor.task_result import TaskResult as AnsibleTaskResult

from ansible_collections.ansible.mockable.plugins.module_utils.mockable import (
    get_mockable_vars,
    mock_task,
    get_task_mockable_configuration,
    get_mockable_configuration,
    get_mockable_filename,
    result_to_nice_dict,
    get_mockable_scenario,
)


class CallbackModule(CallbackBase):
    def __init__(self, display=None, options=None):
        Display().display("ansible.mockable.mockable callback")
        super().__init__()
        self.mockable_vars = {}
        self.mockable_configuration = {}
        self.mockable_data = {}

    def v2_playbook_on_play_start(self, play):
        self.mockable_vars = get_mockable_vars(play)
        self.mockable_configuration = get_mockable_configuration(self.mockable_vars)
        self.mockable_filename = get_mockable_filename(self.mockable_vars)
        self.mockable_scenario = get_mockable_scenario(self.mockable_vars)
        Display().display(f"self.mocable_configuration = {self.mockable_configuration}")
        Display().display(f"self.mocable_vars = {self.mockable_vars}")
        Display().display(f"self.mockable_filename = {self.mockable_filename}")
        if self.mockable_filename:
            self.mockable_data = {
                "mockable_configuration": [
                    {"scenario": self.mockable_scenario, "tasks": []},
                ]
            }

    def v2_runner_on_start(self, host, task):
        task_mockable_configuration = get_task_mockable_configuration(
            task, self.mockable_configuration
        )
        if task_mockable_configuration:
            task = mock_task(task, task_mockable_configuration)

        super().v2_runner_on_start(host, task)

    def update_mockable_data(self, result: AnsibleTaskResult):
        nice_task = result_to_nice_dict(result)
        self.mockable_data["mockable_configuration"][0]["tasks"].append(nice_task)

    def v2_runner_on_ok(self, result):
        if self.mockable_filename:
            self.update_mockable_data(result)
        super().v2_runner_on_ok(result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        if self.mockable_filename:
            self.update_mockable_data(result)
        super().v2_runner_on_failed(result)

    def v2_runner_on_skipped(self, result):
        if self.mockable_filename:
            self.update_mockable_data(result)
        super().v2_runner_on_skipped(result)

    def v2_playbook_on_stats(self, stats):
        with open(self.mockable_filename, "w") as file:
            yaml.dump(self.mockable_data, file, indent=2)
