from enum import Enum
import os
from firecrest.filesystem.ops.commands.base_command_error_handling import (
    BaseCommandErrorHandling,
)
from lib.ssh_clients.ssh_client import BaseCommand

UTILITIES_TIMEOUT = 5


class TarCommand(BaseCommand, BaseCommandErrorHandling):

    class Operation(str, Enum):
        compress = "compress"
        extract = "extract"

    def __init__(
        self,
        source_path: str,
        target_path: str,
        dereference: bool = False,
        operation: Operation = Operation.compress,
    ) -> None:
        super().__init__()
        self.target_path = target_path
        self.source_path = source_path
        self.dereference = dereference
        self.operation = operation

    def get_command(
        self,
    ) -> str:

        match self.operation:
            case TarCommand.Operation.compress:
                return self.get_compress_command()
            case TarCommand.Operation.extract:
                return self.get_extract_command()

    def get_compress_command(self) -> str:
        options = ""
        if self.dereference:
            options += "--dereference"

        source_dir = os.path.dirname(self.source_path)
        source_file = os.path.basename(self.source_path)

        return f"timeout {UTILITIES_TIMEOUT} tar {options} -czvf '{self.target_path}' -C '{source_dir}' '{source_file}'"

    def get_extract_command(self) -> str:

        return f"timeout {UTILITIES_TIMEOUT} tar -xzf '{self.source_path}' -C '{self.target_path}'"

    def parse_output(self, stdout: str, stderr: str, exit_status: int):
        if exit_status != 0:
            super().error_handling(stderr, exit_status)

        return stdout
