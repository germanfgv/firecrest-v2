from typing import List

# configs
from firecrest.config import HPCCluster

# models
from lib.models import CamelModel
from lib.scheduler_clients.slurm.models import (
    SlurmNode,
    SlurmPartitions,
    SlurmReservations,
)


class GetSystemsResponse(CamelModel):
    systems: List[HPCCluster]


class GetNodesResponse(CamelModel):
    nodes: List[SlurmNode]


class GetPartitionsResponse(CamelModel):
    partitions: List[SlurmPartitions]


class GetReservationsResponse(CamelModel):
    reservations: List[SlurmReservations]


class PosixIdentified(CamelModel):
    id: str
    name: str


class UserInfoResponse(CamelModel):
    user: PosixIdentified
    group: PosixIdentified
    groups: List[PosixIdentified]
