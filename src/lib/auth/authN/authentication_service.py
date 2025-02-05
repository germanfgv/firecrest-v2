# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

from abc import ABC, abstractmethod


class AuthenticationService(ABC):

    @abstractmethod
    async def authenticate(self, access_token: str):
        pass
