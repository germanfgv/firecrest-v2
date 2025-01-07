from abc import ABC, abstractmethod


class AuthorizationService(ABC):

    @abstractmethod
    async def authorize(self, resource_name: str, access_token: str):
        pass
