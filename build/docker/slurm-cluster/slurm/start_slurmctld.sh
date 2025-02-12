#!/bin/bash
while true; do
   sleep 1
   t=$(tail -n 2 /var/log/slurm/slurmdbd.log | grep started)
   # continue if succesful
   if [ "$t" != "" ]; then
     break
   fi
   echo "Slurmdbd not ready, retrying..."
done

# Wait for keyklog certificate to be downloaded
while [ ! -f /etc/slurm/jwks.json ]
do
  sleep 2
done

sleep 1
echo "Slurmdbd ready, create cluster"
sacctmgr --immediate create cluster cluster
echo "Slurmdbd, create account 'fireuser' and add firesrv"
sacctmgr --immediate create account name=staff
sacctmgr --immediate create account name=users
sacctmgr --immediate create account name=service-accounts
sacctmgr --immediate create user name=fireuser account=staff
sacctmgr --immediate create user name=fireuser account=users
sacctmgr --immediate create user name=firesrv account=staff
sacctmgr --immediate create user name=firesrv account=service-accounts

echo "Starting slurmctld"
slurmctld  -D
