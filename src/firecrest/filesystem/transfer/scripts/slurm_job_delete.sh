#!/bin/bash 

{{sbatch_directives}}

echo $(date -u) "Delete Files Job (id:${SLURM_JOB_ID})"

status=$(rm -R  -- '{{path}}')
if [[ "$?" == '0' ]]
then
    echo $(date -u) "Files were successfully deleted."
    exit 0 
else 
    echo $(date -u) "Unable to delete files exit code:${?} error: ${status}" >&2
    exit $? 
fi

