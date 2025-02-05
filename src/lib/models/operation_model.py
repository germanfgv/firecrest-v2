# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

# models
from lib.models.base_model import CamelModel


class OperationFail(CamelModel):
    error_description: str
    stdout_message: str
    stderr_message: str
