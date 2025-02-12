# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

from abc import ABC, abstractmethod


class SSHKeysProvider(ABC):

    @abstractmethod
    async def get_keys(self, username: str, jwt_token: str):
        pass
