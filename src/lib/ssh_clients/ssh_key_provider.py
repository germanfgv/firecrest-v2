from abc import ABC, abstractmethod


class SSHKeysProvider(ABC):

    @abstractmethod
    async def get_keys(self, jwt_token: str):
        pass
