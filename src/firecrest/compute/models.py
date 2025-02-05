# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

from typing import List, Optional

# models
from lib.models import CamelModel
from lib.scheduler_clients.models import JobSubmitRequestModel
from lib.scheduler_clients.slurm.models import (
    SlurmJob,
    SlurmJobDescription,
    SlurmJobMetadata,
)


class PostJobSubmitRequest(JobSubmitRequestModel):
    job: SlurmJobDescription


class GetJobResponse(CamelModel):
    jobs: Optional[List[SlurmJob]] = None


class GetJobMetadataResponse(CamelModel):
    jobs: Optional[List[SlurmJobMetadata]] = None


class PostJobSubmissionResponse(CamelModel):
    job_id: Optional[int] = None


class PostJobAttachRequest(CamelModel):
    command: str = None
