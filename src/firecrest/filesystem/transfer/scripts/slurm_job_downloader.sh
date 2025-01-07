#!/bin/bash 

{{sbatch_directives}}

echo $(date -u) "Ingress File Transfer Job (id:${SLURM_JOB_ID})"
echo $(date -u) "Waiting till file to tranfer is available..."
for i in `seq 1440` 
do 
    status=$(curl --silent --head -o /dev/null --silent -Iw '%{http_code}' "{{download_head_url}}")
    if [[ "$status" == '200' ]]
        then
                echo $(date -u) "File to transfer found in S3 bucket"
                echo $(date -u) "Downloading file to: {{target_path}} ..."
                curl_output=$(curl --compressed --silent -o {{target_path}} "{{download_url}}" -w '%{size_download}')
                if [ $? -ne 0 ] 
                    then 
                        echo $(date -u) "File download completed with error" 
                    fi

                # Convert to MB to make logs more readable
                download_bytes=$(echo | awk -v download_bytes="$curl_output" ' { printf "%0.3f\n", (download_bytes/1024/1024); } ')              
                if [ $? -eq 0 ] 
                    then 
                        echo $(date -u) "File was successfully downloaded (size: ${download_bytes}MB)" 
                    else 
                        echo $(date -u) "Unable to download file" >&2 
                    fi
                break
        fi
    sleep 60;
done 
