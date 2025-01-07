#!/bin/bash
##
##  Copyright (c) 2019-2023, ETH Zurich. All rights reserved.
##
##  Please, refer to the LICENSE file in the root directory.
##  SPDX-License-Identifier: BSD-3-Clause
##


# Wait for keyklog certificate to be downloaded
while [ ! -f /etc/slurm/jwks.json ]
do
  sleep 2
done


# start slurmrestd
slurmrestd -f /etc/slurm/slurmrestd.conf 0.0.0.0:6820
