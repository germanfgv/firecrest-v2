from abc import ABC, abstractmethod


class AuthenticationService(ABC):

    @abstractmethod
    async def authenticate(self, access_token: str):
        pass
