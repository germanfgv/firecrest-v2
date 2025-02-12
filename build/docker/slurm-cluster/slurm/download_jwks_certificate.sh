#!/bin/bash

# Wait for keyklog certificate to be downloaded
while [ ! -f /etc/slurm/jwks.json ]
do
  if python3 --version ;
    then
    python3 /download_jwks_certificates_3.py "${OIDC_CERT_URLS}" /etc/slurm/jwks.json
  else
    python /download_jwks_certificates.py "${OIDC_CERT_URLS}" /etc/slurm/jwks.json
  fi
  sleep 2
done

#Replace with merged multi cert verions

