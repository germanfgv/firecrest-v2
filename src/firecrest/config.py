from enum import Enum
import os
from pathlib import Path
from typing import Dict, Tuple, Type
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from datetime import datetime
from functools import lru_cache
from typing import List, Optional

from lib.models.base_model import CamelModel
from lib.models.config_model import Oidc


class LoadFileSecretStr(SecretStr):

    def __init__(self, secret_value: str) -> None:
        if secret_value.startswith("secret_file:"):
            secrets_path = Path(secret_value[12:]).expanduser()
            if not secrets_path.exists() or not secrets_path.is_file:
                raise FileNotFoundError(f"Secret file: {secrets_path} not found!")
            secret_value = secrets_path.read_text("utf-8").strip()
        super().__init__(secret_value)


class MultipartUpload(BaseModel):
    use_split: Optional[bool] = False
    max_part_size: Optional[int] = 2 * 1024 * 1024 * 1024
    parallel_runs: Optional[int] = 3
    tmp_folder: Optional[str] = "tmp"


class BucketLifestyleConfiguration(BaseModel):
    days: Optional[int] = 10

    def to_json(self):
        return {
            "Rules": [
                {
                    "ID": "ExpireObjects",
                    "Prefix": "",
                    "Status": "Enabled",
                    "Expiration": {"Days": self.days},
                }
            ]
        }


class Storage(BaseModel):
    name: str
    private_url: str
    public_url: str
    access_key_id: str
    secret_access_key: LoadFileSecretStr
    region: str
    ttl: int
    tenant: Optional[str] = None
    multipart: Optional[MultipartUpload] = MultipartUpload()
    bucket_lifecycle_configuration: Optional[BucketLifestyleConfiguration] = (
        BucketLifestyleConfiguration()
    )
    max_ops_file_size: Optional[int] = 5 * 1024 * 1024


class SchedulerType(str, Enum):
    slurm = "slurm"


class FileSystemDataType(str, Enum):
    users = "users"
    store = "store"
    archive = "archive"
    apps = "apps"
    scratch = "scratch"
    project = "project"


class Scheduler(CamelModel):
    type: SchedulerType
    version: Optional[str] = None
    api_url: Optional[str] = None
    api_version: Optional[str] = None
    timeout: Optional[int] = 10


class ServiceAccount(CamelModel):
    client_id: str
    secret: LoadFileSecretStr


class ClusterNodesHealth(CamelModel):
    available: int = 0
    total: int = 0


class HealthCheckType(str, Enum):
    scheduler = "scheduler"
    filesystem = "filesystem"
    ssh = "ssh"


class BaseServiceHealth(CamelModel):
    service_type: HealthCheckType
    last_checked: Optional[datetime] = None
    latency: Optional[float] = None
    healthy: Optional[bool] = False
    message: Optional[str] = None


class SchedulerServiceHealth(BaseServiceHealth):
    nodes: Optional[ClusterNodesHealth] = None


class FilesystemServiceHealth(BaseServiceHealth):
    path: Optional[str] = None


class SSHServiceHealth(BaseServiceHealth):
    pass


class ClusterProbing(CamelModel):
    interval: int
    timeout: int


class FileSystem(CamelModel):
    path: str
    data_type: FileSystemDataType
    default_work_dir: Optional[bool] = False


class SSHTimeouts(CamelModel):
    connection: Optional[int] = 5
    login: Optional[int] = 5
    command_execution: Optional[int] = 5
    idle_timeout: Optional[int] = 60
    keep_alive: Optional[int] = 5


class SSHClientPool(CamelModel):
    host: str
    port: int
    max_clients: Optional[int] = 100
    timeout: Optional[SSHTimeouts] = SSHTimeouts()


class HPCCluster(CamelModel):
    name: str
    ssh: SSHClientPool
    scheduler: Scheduler
    service_account: ServiceAccount = Field(exclude=True)
    servicesHealth: Optional[
        List[SchedulerServiceHealth | FilesystemServiceHealth | SSHServiceHealth]
    ] = None
    probing: Optional[ClusterProbing] = None
    file_systems: Optional[List[FileSystem]] = None
    datatransfer_jobs_directives: Optional[List[str]] = []


class OpenFGA(CamelModel):
    url: str
    timeout: Optional[int] = 1
    max_connections: Optional[int] = 100


class SSHKeysService(CamelModel):
    url: str
    max_connections: Optional[int] = 100


class SSHStaticKeys(CamelModel):
    private_key: LoadFileSecretStr
    public_key: str


class Auth(CamelModel):
    authentication: Oidc = None
    authorization: Optional[OpenFGA] = None


class Settings(BaseSettings):
    # General variables
    environment: str = "production"
    admin_email: str = "support@cscs.ch"
    # App variables
    app_debug: bool = False
    app_name: str = "FirecREST - APIs"
    app_description: str = "FirecREST - APIs"
    app_version: str = "0.0.1"
    # Service variables
    service_ws: str = ""
    service_name: str = "firecrest-api"
    # Logging variables
    logging_level: str = "DEBUG"
    # APIs variables
    apis_root_path: str = ""
    doc_servers: Optional[List[Dict]] = None
    auth: Auth = None
    # Slurm
    clusters: List[HPCCluster] = []
    # SSH Service
    ssh_credentials: SSHKeysService | SSHStaticKeys
    # storage
    storage: Storage = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", secrets_dir="/run/secrets/"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        yaml_file = os.getenv("YAML_CONFIG_FILE", None)
        if yaml_file is None or yaml_file == "":
            raise EnvironmentError("Missing YAML_CONFIG_FILE environment variable")
        return (
            init_settings,
            YamlConfigSettingsSource(
                settings_cls=settings_cls,
                yaml_file=yaml_file,
                yaml_file_encoding="utf-8",
            ),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


@lru_cache()
def get_settings():
    return Settings()
