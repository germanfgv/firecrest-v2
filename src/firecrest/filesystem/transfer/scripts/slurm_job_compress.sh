#!/bin/bash 
# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause


{{sbatch_directives}}

echo $(date -u) "Compress Files Job (id:${SLURM_JOB_ID})"

status=$(tar {{ options }} -czvf '{{target_path}}' -C '{{source_dir}}'  '{{source_file}}')
if [[ "$?" == '0' ]]
then
    echo $(date -u) "Files were successfully compressed."
    exit 0 
else 
    echo $(date -u) "Unable to compress files exit code:${?} error: ${status}" >&2
    exit $? 
fi

