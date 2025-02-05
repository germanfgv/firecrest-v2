from typing import Any, Optional

# models
from firecrest.filesystem.models import FilesystemRequestBase
from lib.models import CamelModel


class PostFileUploadRequest(FilesystemRequestBase):
    file_name: str
    account: Optional[str] = None
    file_size: int


class PostFileDownloadRequest(FilesystemRequestBase):
    account: Optional[str] = None


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
    parts_upload_urls: list
    complete_upload_url: str
    max_part_size: int
    transfer_job: TransferJob


class DownloadFileResponse(CamelModel):
    download_url: str
    transfer_job: TransferJob


class CopyRequest(FilesystemRequestBase):
    target_path: str
    account: Optional[str] = None


class CopyResponse(CamelModel):
    transfer_job: TransferJob


class DeleteResponse(CamelModel):
    transfer_job: TransferJob


class MoveRequest(FilesystemRequestBase):
    target_path: str
    account: Optional[str] = None


class MoveResponse(CamelModel):
    transfer_job: TransferJob
