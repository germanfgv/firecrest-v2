# models
from lib.models.base_model import CamelModel


class OperationFail(CamelModel):
    error_description: str
    stdout_message: str
    stderr_message: str
