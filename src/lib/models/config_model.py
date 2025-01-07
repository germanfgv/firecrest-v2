from typing import List, Optional
from lib.models.base_model import CamelModel


class Oidc(CamelModel):
    scopes: Optional[dict] = {}
    token_url: str
    public_certs: List[str] = []
