# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

from lib.exceptions import SlurmError
from lib.scheduler_clients.slurm.cli_commands.scontrol_base import ScontrolBase


class ScontrolBatchScriptCommand(ScontrolBase):

    def __init__(self, job_id: str = None) -> None:
        super().__init__()
        self.job_id = job_id

    def get_command(self) -> str:
        cmd = [super().get_command()]
        cmd += [f"write batch_script {self.job_id} -"]
        return " ".join(cmd)

    def parse_output(self, stdout: str, stderr: str, exit_status: int = 0):
        if exit_status != 0:
            raise SlurmError(
                f"Unexpected Slurm command response. exit_status:{exit_status} std_err:{stderr}"
            )

        return [
            {
                "jobId": self.job_id,
                "script": stdout,
            }
        ]
