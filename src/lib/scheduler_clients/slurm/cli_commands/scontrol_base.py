from abc import abstractmethod
from lib.ssh_clients.ssh_client import BaseCommand


class ScontrolBase(BaseCommand):

    def get_command(self) -> str:
        cmd = ["scontrol"]
        return " ".join(cmd)

    @abstractmethod
    def parse_output(self, stdout: str, stderr: str, exit_status: int = 0):
        pass
