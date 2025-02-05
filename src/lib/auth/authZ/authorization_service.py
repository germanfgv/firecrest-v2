# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

from abc import ABC, abstractmethod


class AuthorizationService(ABC):

    @abstractmethod
    async def authorize(self, resource_name: str, access_token: str):
        pass
