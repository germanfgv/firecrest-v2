from typing import Any

# models
from firecrest.filesystem.models import FilesystemRequestBase
from lib.models import CamelModel


class PostFileUploadRequest(FilesystemRequestBase):
    file_name: str


class PostFileDownloadRequest(FilesystemRequestBase):
    pass


class PostXferInternalOperationApiResponse(CamelModel):
    operation: Any


class TransferJobLogs(CamelModel):
    output_log: str
    error_log: str


class TransferJob(CamelModel):
    job_id: int
    system: str
    working_directory: str
    logs: TransferJobLogs


class UploadFileResponse(CamelModel):
    upload_url: str
    transfer_job: TransferJob


class DownloadFileResponse(CamelModel):
    download_url: str
    transfer_job: TransferJob


class CopyRequest(FilesystemRequestBase):
    target_path: str


class CopyResponse(CamelModel):
    transfer_job: TransferJob


class DeleteResponse(CamelModel):
    transfer_job: TransferJob


class MoveRequest(FilesystemRequestBase):
    target_path: str


class MoveResponse(CamelModel):
    transfer_job: TransferJob
