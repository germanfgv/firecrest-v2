from enum import Enum
from typing import Optional

# models
from firecrest.filesystem.models import FilesystemRequestBase
from lib.models import CamelModel


class ContentUnit(str, Enum):
    lines = "lines"
    bytes = "bytes"


class File(CamelModel):
    name: str
    type: str
    link_target: Optional[str]
    user: str
    group: str
    permissions: str
    last_modified: str
    size: str


class FileContent(CamelModel):
    content: str
    content_type: ContentUnit
    start_position: int
    end_position: int


class FileChecksum(CamelModel):
    algorithm: str = "SHA-256"
    checksum: str


class FileStat(CamelModel):
    # message: str
    mode: int
    ino: int
    dev: int
    nlink: int
    uid: int
    gid: int
    size: int
    atime: int
    ctime: int
    mtime: int
    # birthtime: int


class PatchFile(CamelModel):
    message: str
    new_filepath: str
    new_permissions: str
    new_owner: str


class PatchFileMetadataRequest(CamelModel):
    new_filename: Optional[str] = None
    new_permissions: Optional[str] = None
    new_owner: Optional[str] = None


class GetDirectoryLsResponse(CamelModel):
    output: Optional[list[File]]


class GetFileHeadResponse(CamelModel):
    output: Optional[FileContent]


class GetFileTailResponse(CamelModel):
    output: Optional[FileContent]


class GetFileChecksumResponse(CamelModel):
    output: Optional[FileChecksum]


class GetFileTypeResponse(CamelModel):
    output: Optional[str]


class GetFileStatResponse(CamelModel):
    output: Optional[FileStat]


class PatchFileMetadataResponse(CamelModel):
    output: Optional[PatchFile]


class PutFileChmodRequest(CamelModel):
    path: str
    mode: str


class PutFileChmodResponse(CamelModel):
    output: Optional[File]


class PutFileChownRequest(FilesystemRequestBase):
    owner: Optional[str] = ""
    group: Optional[str] = ""


class PutFileChownResponse(CamelModel):
    output: Optional[File]


class PostMakeDirRequest(FilesystemRequestBase):
    parent: Optional[bool] = False


class PostFileSymlinkRequest(FilesystemRequestBase):
    link_path: str


class PostFileSymlinkResponse(CamelModel):
    output: Optional[File]


class GetViewFileResponse(CamelModel):
    output: Optional[str]


class PostMkdirResponse(CamelModel):
    output: Optional[File]


class PostCompressRequest(FilesystemRequestBase):
    target_path: str
    dereference: Optional[bool] = False


class PostExtractRequest(FilesystemRequestBase):
    target_path: str
