#!/bin/bash

# Wait for keyklog certificate to be downloaded
while [ ! -f /etc/slurm/jwks.json ]
do
  sleep 2
done


# start slurmrestd
slurmrestd -f /etc/slurm/slurmrestd.conf 0.0.0.0:6820
