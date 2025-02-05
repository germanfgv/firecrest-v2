from abc import ABC, abstractmethod


class SSHKeysProvider(ABC):

    @abstractmethod
    async def get_keys(self, username: str, jwt_token: str):
        pass
