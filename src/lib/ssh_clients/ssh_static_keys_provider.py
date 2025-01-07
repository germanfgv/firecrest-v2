from lib.ssh_clients.ssh_key_provider import SSHKeysProvider


class SSHStaticKeysProvider(SSHKeysProvider):

    def __init__(self, private_key: str, public_key: str):
        self.private_key = private_key
        self.public_key = public_key

    async def get_keys(self, jwt_token: str):
        return {
            "private": self.private_key.get_secret_value(),
            "public": self.public_key,
        }
