#!/bin/bash 

{{sbatch_directives}}

echo $(date -u) "Copy Files Job (id:${SLURM_JOB_ID})"

status=$(cp  -- '{{source_path}}' '{{target_path}}')
if [[ "$?" == '0' ]]
then
    echo $(date -u) "Files were successfully copied."
    exit 0 
else 
    echo $(date -u) "Unable to copy files exit code:${?} error: ${status}" >&2
    exit $? 
fi

