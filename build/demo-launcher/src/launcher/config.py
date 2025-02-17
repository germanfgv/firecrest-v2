import sys
from typing import Dict, List, Optional
from humps import camelize
from pydantic import BaseModel, ConfigDict

sys.path.append("../../../src")
sys.path.append("../")
from firecrest.config import Settings, HPCCluster, ServiceAccount, SSHClientPool


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=camelize,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True,
    )


class UnsafeSSHClientPool(SSHClientPool):
    pass


class UnsafeSSHUserKeys(CamelModel):
    private_key: str
    public_cert: Optional[str] = None


class UnsafeServiceAccount(ServiceAccount):
    client_id: str
    secret: str


class UnsafeHPCCluster(HPCCluster):
    service_account: UnsafeServiceAccount
    ssh: UnsafeSSHClientPool


class UnsafeSettings(Settings):
    ssh_credentials: Dict[str, UnsafeSSHUserKeys]
    clusters: List[UnsafeHPCCluster] = []
