from humps import camelize
from pydantic import BaseModel, ConfigDict


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=camelize,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True,
    )
