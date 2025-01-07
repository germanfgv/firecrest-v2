#!/bin/bash

{{sbatch_directives}}

echo $(date -u) "Move Files Job (id:${SLURM_JOB_ID})"

status=$(mv  -- '{{source_path}}' '{{target_path}}')
if [[ "$?" == '0' ]]
then
    echo $(date -u) "Files were successfully moved."
    exit 0
else
    echo $(date -u) "Unable to move files exit code:${?} error: ${status}" >&2
    exit $?
fi

