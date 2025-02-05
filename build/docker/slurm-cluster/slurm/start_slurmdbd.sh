#!/bin/bash

while true; do
   echo "use mysql;" | mysql -u root
   # continue if succesful
   if [ "$?" == 0 ]; then
     break
   fi
   sleep 1
done

# Wait for keyklog certificate to be downloaded
while [ ! -f /etc/slurm/jwks.json ]
do
  sleep 2
done

echo "127.0.0.1 cluster" >> /etc/hosts

echo "CREATE USER 'slurmdb'@'localhost' IDENTIFIED BY 'slurmdbpass';" | mysql -u root
echo "CREATE DATABASE slurmdb; GRANT ALL PRIVILEGES ON slurmdb.* TO 'slurmdb'@'localhost';" | mysql -u root

slurmdbd -D
