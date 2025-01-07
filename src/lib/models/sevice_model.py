from enum import Enum


class ServiceName(str, Enum):
    compute = "compute"
    storage = "storage"
    tasks = "tasks"
    status = "status"
    utilities = "utilities"
