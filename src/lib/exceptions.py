class SchedulerError(Exception):
    error_msg: str

    def __init__(self, error):
        super().__init__(error)
        self.error_msg = error


class SlurmError(SchedulerError):
    pass


class SlurmAuthTokenError(SlurmError):
    pass


class SSHServiceError(Exception):
    pass


class SSHCredentials(Exception):
    pass
