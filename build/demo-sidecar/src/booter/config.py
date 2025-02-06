import sys
from typing import Dict
from humps import camelize
from pydantic import BaseModel, ConfigDict

sys.path.append("../../../src")
from firecrest.config import Settings


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=camelize,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True,
    )


class UnsafeSSHUserKeys(CamelModel):
    private_key: str
    public_key: str


class UnsafeSettings(Settings):

    ssh_credentials: Dict[str, UnsafeSSHUserKeys]
