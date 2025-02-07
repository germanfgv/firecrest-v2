#!/bin/bash 
# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause


{{sbatch_directives}}

echo $(date -u) "Compress Files Job (id:${SLURM_JOB_ID})"

status=$(cd {{ source_dir }})
if [[ "$?" == '0' ]]
then
    echo $(date -u) "Changed to {{ source_dir }}"
else 
    echo $(date -u) "Unable to compress files exit code:${?} error: ${status}" >&2
    exit $? 
fi

status=$(find . -type f -regex '{{pattern}}' -print0 | tar {{ options }} -czvf '{{target_path}}' --null --files-from - )
if [[ "$?" == '0' ]]
then
    echo $(date -u) "Files were successfully compressed."
    exit 0 
else 
    echo $(date -u) "Unable to compress files exit code:${?} error: ${status}" >&2
    exit $? 
fi
