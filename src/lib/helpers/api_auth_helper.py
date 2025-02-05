# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

# request vars
from lib.request_vars import g

# models
from lib.models import ApiAuthModel


class ApiAuthHelper:

    def __init__(self):
        pass

    @staticmethod
    def is_authenticated() -> bool:
        if hasattr(g(), "auth"):
            return g().auth is not None
        return False

    @staticmethod
    def get_access_token() -> str | None:
        if ApiAuthHelper.is_authenticated():
            return g().access_token
        return None

    @staticmethod
    def set_access_token(access_token: str):
        g().access_token = access_token
        return access_token

    @staticmethod
    def get_auth() -> ApiAuthModel | None:
        if ApiAuthHelper.is_authenticated():
            return g().auth
        return None

    @staticmethod
    def set_auth(auth: ApiAuthModel):
        g().auth = auth
        return auth

    @staticmethod
    def get_auth_username() -> str | None:
        if ApiAuthHelper.is_authenticated():
            return g().auth.username
        return None
