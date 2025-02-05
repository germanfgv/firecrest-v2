# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

from lib.exceptions import SlurmError
import re
from datetime import datetime

from lib.scheduler_clients.slurm.cli_commands.scontrol_base import ScontrolBase


def _null_to_none(string: str):
    if string == "(null)":
        return None
    return string


class ScontrolReservationCommand(ScontrolBase):

    def get_command(self) -> str:
        cmd = [super().get_command()]
        cmd += ["-a show -o reservations"]
        return " ".join(cmd)

    def parse_output(self, stdout: str, stderr: str, exit_status: int = 0):
        if exit_status != 0:
            raise SlurmError(
                f"Unexpected Slurm command response. exit_status:{exit_status} std_err:{stderr}"
            )

        if stdout.lower().startswith("no reservations"):
            return []

        attributes = [
            "ReservationName",
            "State",
            "Nodes",
            "StartTime",
            "EndTime",
            "Features",
        ]
        convert_date = [
            "StartTime",
            "EndTime",
        ]

        reservations = []

        for reservation_str in stdout.split("\n"):
            if len(reservation_str) == 0:
                continue
            reservation = {}
            for attr_name in attributes:
                attr_match = re.search(rf"{attr_name}=(\S+)", reservation_str)
                if attr_match:
                    if attr_name in convert_date:
                        date = datetime.fromisoformat(attr_match.group(1))
                        reservation[attr_name] = date.timestamp()
                    else:
                        reservation[attr_name] = _null_to_none(attr_match.group(1))
                else:
                    raise ValueError(
                        f"Could not parse attribute '{attr_name}' in "
                        f"'{reservation_str}'"
                    )

            reservations.append(reservation)

        return reservations
