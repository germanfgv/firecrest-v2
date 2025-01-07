from typing import Optional

from pydantic import AliasChoices, Field
from lib.models.base_model import CamelModel


class FilesystemRequestBase(CamelModel):
    path: Optional[str] = Field(
        validation_alias=AliasChoices("sourcePath", "source_path")
    )
