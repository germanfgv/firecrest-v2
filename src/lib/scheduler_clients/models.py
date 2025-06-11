# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

# models
from typing import List, Optional
from lib.models import CamelModel


class JobStatus(CamelModel):
    state: str
    stateReason: Optional[str] = None
    exitCode: Optional[int] = None
    interruptSignal: Optional[int] = None


class JobTime(CamelModel):
    elapsed: Optional[int]
    start: Optional[int] = None
    end: Optional[int] = None
    suspended: Optional[int] = None
    limit: Optional[int] = None


class JobTask(CamelModel):
    id: str
    name: str
    status: JobStatus
    time: JobTime


class JobModel(CamelModel):
    job_id: int
    name: str
    status: JobStatus
    tasks: Optional[List[JobTask]] = None
    time: JobTime
    account: Optional[str]
    allocation_nodes: int
    cluster: str
    group: str
    nodes: str
    partition: str
    kill_request_user: Optional[str] = None
    user: Optional[str]
    working_directory: str
    priority: Optional[int] = None


class JobMetadataModel(CamelModel):
    pass


class JobDescriptionModel(CamelModel):
    pass


class JobSubmitRequestModel(CamelModel):
    pass


class NodeModel(CamelModel):
    pass


class ReservationModel(CamelModel):
    pass


class PartitionModel(CamelModel):
    pass
