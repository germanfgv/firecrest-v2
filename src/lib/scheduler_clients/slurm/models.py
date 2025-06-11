# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

from typing import Dict, List, Optional

from pydantic import (
    AliasChoices,
    Field,
    RootModel,
)

# models
from lib.models.base_model import CamelModel
from lib.scheduler_clients.models import (
    JobMetadataModel,
    JobModel,
    JobDescriptionModel,
    JobStatus,
    JobTask,
    JobTime,
    NodeModel,
    PartitionModel,
    ReservationModel,
)


class SlurmInt(RootModel):
    root: int | None

    # starting from v0.0.40 slurm api represents int with a complex object
    # e.s. {"set": True, "infinite": False, "number": 0},
    def __init__(self, **kwargs):
        if kwargs["set"] == "False":
            super().__init__(None)
        else:
            super().__init__(kwargs["number"])


def slurm_int_to_int(v) -> Optional[int]:
    # starting from v0.0.40 slurm api represents int with a complex object
    # e.s. {"set": True, "infinite": False, "number": 0},
    if v is None or isinstance(v, int) or isinstance(v, float):
        return v

    if isinstance(v, str):
        try:
            # FIXME: not sure if this is always int or can be float
            return int(v)
        except ValueError:
            raise ValueError(f"Invalid SlurmInt value: {v!r}")

    if isinstance(v, dict):
        if not v.get("set", True):
            return None

        return int(v.get("number"))

    raise ValueError(f"Invalid SlurmInt value: {v!r}")


class SlurmJobDescription(JobDescriptionModel):
    name: Optional[str] = Field(default=None, description="Name for the job")
    account: Optional[str] = Field(
        default=None, description="Charge job resources to specified account"
    )
    current_working_directory: str = Field(
        alias="working_directory", description="Job working directory"
    )
    standard_input: Optional[str] = Field(
        default=None, description="Standard input file name"
    )
    standard_output: Optional[str] = Field(
        default=None, description="Standard output file name"
    )
    standard_error: Optional[str] = Field(
        default=None, description="Standard error file name"
    )
    environment: Optional[Dict[str, str] | List[str]] = Field(
        alias="env",
        default={"F7T_version": "v2.0.0"},
        description="Dictionary of environment variables to set in the job context",
    )
    constraints: Optional[str] = Field(default=None, description="Job constraints")
    script: str = Field(default=None, description="Script for the job")
    script_path: str = Field(
        default=None, description="Path to the job in target system"
    )


class SlurmJobMetadata(JobMetadataModel):
    job_id: int
    script: Optional[str] = None
    standard_input: Optional[str] = Field(
        validation_alias=AliasChoices("StdIn", "standardInput"), default=None
    )
    standard_output: Optional[str] = Field(
        validation_alias=AliasChoices("StdOut", "standardOutput"), default=None
    )
    standard_error: Optional[str] = Field(
        validation_alias=AliasChoices("StdErr", "standardError"), default=None
    )


class JobStatusSlurm(JobStatus):
    def __init__(self, **kwargs):
        if isinstance(kwargs["state"], list):
            if len(kwargs["state"]) > 0:
                kwargs["state"] = kwargs["state"][0]
            else:
                kwargs["state"] = None

        for field in ["exitCode", "interruptSignal"]:
            if field in kwargs and kwargs[field] is not None:
                kwargs[field] = slurm_int_to_int(kwargs[field])

        super().__init__(**kwargs)


class JobTimeSlurm(JobTime):
    def __init__(self, **kwargs):
        for field in ["elapsed", "start", "end", "suspended", "limit"]:
            if field in kwargs and kwargs[field] is not None:
                kwargs[field] = slurm_int_to_int(kwargs[field])

        super().__init__(**kwargs)


class JobTaskSlurm(JobTask):

    time: JobTimeSlurm

    def __init__(self, **kwargs):
        # Custom task field definition
        if "step" in kwargs:
            kwargs["id"] = kwargs["step"]["id"]
            kwargs["name"] = kwargs["step"]["name"]

        if "exit_code" in kwargs:
            interruptSignal = None
            exitCode = None

            if kwargs["exit_code"] and "return_code" in kwargs["exit_code"]:
                exitCode = kwargs["exit_code"]["return_code"]

            if kwargs["exit_code"] and "signal" in kwargs["exit_code"]:
                interruptSignal = kwargs["exit_code"]["signal"]["id"]

            kwargs["status"] = JobStatusSlurm(
                state=kwargs["state"],
                stateReason=None,
                exitCode=exitCode,
                interruptSignal=interruptSignal,
            )

        super().__init__(**kwargs)


class SlurmJob(JobModel):

    tasks: Optional[List[JobTaskSlurm]] = None
    time: JobTimeSlurm

    def __init__(self, **kwargs):
        # Custom status field definition
        if "exit_code" in kwargs:
            interruptSignal = None
            exitCode = None

            if kwargs["exit_code"] and "return_code" in kwargs["exit_code"]:
                exitCode = kwargs["exit_code"]["return_code"]

            if kwargs["exit_code"] and "signal" in kwargs["exit_code"]:
                interruptSignal = kwargs["exit_code"]["signal"]["id"]

            kwargs["status"] = JobStatusSlurm(
                state=kwargs["state"]["current"],
                stateReason=kwargs["state"]["reason"],
                exitCode=exitCode,
                interruptSignal=interruptSignal,
            )
        if "steps" in kwargs:
            kwargs["tasks"] = kwargs["steps"]

        if "priority" in kwargs:
            kwargs["priority"] = slurm_int_to_int(kwargs["priority"])

        super().__init__(**kwargs)


class SlurmNode(NodeModel):
    sockets: int
    cores: int
    threads: int
    cpus: int
    cpu_load: Optional[float] = None
    free_memory: Optional[int] = None
    features: str | List[str]
    name: str
    address: str
    hostname: str
    state: str | List[str]  # e.g. ["IDLE", "RESERVED"]
    partitions: List[str]
    weight: int
    slurmd_version: Optional[str] = None
    alloc_memory: Optional[int] = None
    alloc_cpus: Optional[int] = None
    idle_cpus: Optional[int] = None


class SlurmPing(CamelModel):
    hostname: Optional[str] = None
    pinged: Optional[str] = None
    latency: Optional[int] = None
    mode: Optional[str] = None


class SlurmPartition(RootModel):
    root: List[str]

    def __init__(self, **kwargs):
        super().__init__(kwargs["state"])


class SlurmPartitionCPUs(RootModel):
    root: int

    def __init__(self, **kwargs):
        super().__init__(kwargs["total"])


class SlurmPartitions(PartitionModel):
    name: str = Field(validation_alias=AliasChoices("partitionName", "PartitionName"))
    cpus: int | SlurmPartitionCPUs = Field(
        validation_alias=AliasChoices("totalCPUs", "total_cpus", "TotalCPUs")
    )
    total_nodes: int = Field(validation_alias=AliasChoices("totalNodes", "TotalNodes"))
    partition: SlurmPartition | str = Field(
        validation_alias=AliasChoices("state", "State")
    )

    def __init__(self, **kwargs):

        # To allow back compatibility with Slurm API versions <= 0.0.38
        if "total_nodes" not in kwargs and "nodes" in kwargs:
            kwargs["total_nodes"] = kwargs["nodes"]["total"]
        super().__init__(**kwargs)


class SlurmReservations(ReservationModel):
    name: str = Field(
        validation_alias=AliasChoices("reservationName", "ReservationName")
    )
    node_list: str = Field(validation_alias=AliasChoices("nodes", "Nodes", "nodeList"))
    end_time: int | SlurmInt = Field(
        validation_alias=AliasChoices("endTime", "EndTime")
    )
    start_time: int | SlurmInt = Field(
        validation_alias=AliasChoices("startTime", "StartTime")
    )
    features: Optional[str] = Field(validation_alias=AliasChoices("Features"))
