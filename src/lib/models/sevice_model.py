# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

from enum import Enum


class ServiceName(str, Enum):
    compute = "compute"
    storage = "storage"
    tasks = "tasks"
    status = "status"
    utilities = "utilities"
