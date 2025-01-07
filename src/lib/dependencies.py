from fastapi import Request


# helpers
from lib.auth.authN.authentication_service import AuthenticationService
from lib.auth.authZ.authorization_service import AuthorizationService
from lib.helpers.oauth2_client_credentials import Oauth2ClientCredentials
from lib.models.apis.api_auth_model import ApiAuthUser


class AuthDependency(Oauth2ClientCredentials):

    def __init__(
        self,
        authNService: AuthenticationService,
        authZService: AuthorizationService,
        token_url,
        scopes,
    ) -> None:
        self.authN = authNService
        self.authZ = authZService
        super().__init__(token_url=token_url, scopes=scopes)

    async def __call__(self, system_name: str, request: Request):
        token = await super().__call__(request)
        auth: ApiAuthUser = await self.authN.authenticate(token)
        if self.authZ:
            await self.authZ.authorize(auth.username, system_name, token)

        return auth, token

    # To allow for dependency override eq checks for class equality
    def __eq__(self, other):
        return isinstance(other, AuthDependency)

    # To allow for dependency override hash is based on class
    def __hash__(self):
        return hash(AuthDependency.__class__)
