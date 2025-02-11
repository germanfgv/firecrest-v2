from contextlib import asynccontextmanager
import os
from fastapi import Depends, FastAPI, Form


from fastapi.security import HTTPBasic, HTTPBasicCredentials
import jwt
from datetime import datetime, timedelta
from typing import Annotated, Any, Optional
from jose.utils import base64url_encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import yaml
from xmlrpc.client import ServerProxy
from sidecar.config import (
    UnsafeSSHClientPool,
    UnsafeSSHUserKeys,
    UnsafeServiceAccount,
    UnsafeSettings,
)

keys = {}


@asynccontextmanager
async def lifespan(app: FastAPI):

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    keys["private_key_pem"] = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_key = private_key.public_key()
    # public_key_pem = public_key.public_bytes(
    #    encoding=serialization.Encoding.PEM,
    #    format=serialization.PublicFormat.SubjectPublicKeyInfo,
    # )
    public_numbers = public_key.public_numbers()

    keys["public_numbers"] = public_numbers
    keys["kid"] = "42"  # unique key identifier
    yield


app = FastAPI(lifespan=lifespan)


def get_jwk():
    jwk_data = {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "kid": keys["kid"],
        "n": base64url_encode(
            keys["public_numbers"].n.to_bytes(
                (keys["public_numbers"].n.bit_length() + 7) // 8, byteorder="big"
            )
        ),
        "e": base64url_encode(
            keys["public_numbers"].e.to_bytes(
                (keys["public_numbers"].e.bit_length() + 7) // 8, byteorder="big"
            )
        ),
    }
    return jwk_data


security = HTTPBasic(auto_error=False)


# Endpoint 1: Get token
@app.post("/token")
def get_token(
    credentials: Annotated[Optional[HTTPBasicCredentials], Depends(security)],
    grant_type: Optional[str] = Form(default=None),
    client_id: Optional[str] = Form(default=None),
    client_secret: Optional[str] = Form(default=None),
):
    username: str = None
    if client_id:
        username = client_id
    if credentials and credentials.username:
        username = credentials.username

    # Generate JWT token
    expiration = datetime.utcnow() + timedelta(days=360)
    payload = {
        "sub": f"{username}-client",
        "name": username,
        "username": username,
        "preferred_username": username,
        "scope": "firecrest-v2 profile email",
        "exp": expiration,
    }
    headers = {"kid": keys["kid"]}
    token = jwt.encode(
        payload, keys["private_key_pem"], algorithm="RS256", headers=headers
    )

    return {"access_token": token, "token_type": "bearer"}


@app.get("/certs")
def download_certificate():
    return {"keys": [get_jwk()]}


@app.post("/boot")
def post_boot(
    username: Optional[str] = Form(default=None),
    private_key: Optional[str] = Form(default=None),
    public_key: Optional[str] = Form(default=None),
    ssh_hostname: Optional[str] = Form(default=None),
    ssh_port: Optional[str] = Form(default=None),
):

    settings = UnsafeSettings()

    ssh_credential = UnsafeSSHUserKeys(
        **{"private_key": private_key, "public_key": public_key}
    )
    settings.ssh_credentials[username] = ssh_credential

    demo_cluster = settings.clusters[0]
    ssh_client_pool = UnsafeSSHClientPool(**{"host": ssh_hostname, "port": ssh_port})
    service_account = UnsafeServiceAccount(**{"client_id": username, "secret": ""})

    demo_cluster.ssh = ssh_client_pool
    demo_cluster.service_account = service_account

    dump: dict[str, Any] = settings.model_dump()
    settings_file = os.getenv("YAML_CONFIG_FILE", None)
    with open(settings_file, "w") as yaml_file:
        yaml.dump(dump, yaml_file)

    server = ServerProxy("http://localhost:9001/RPC2")
    server.supervisor.startProcess("firecrest")

    return {"message": "Settings saved successfully."}


@app.get("/boot")
def get_boot():

    settings = UnsafeSettings()

    # TODO: inject demo's user settings

    dump: dict[str, Any] = settings.model_dump()
    settings_file = os.getenv("YAML_CONFIG_FILE", None)
    with open(settings_file, "w") as yaml_file:
        yaml.dump(dump, yaml_file)

    server = ServerProxy("http://localhost:9001/RPC2")
    server.supervisor.startProcess("firecrest")

    return {"message": "Settings saved successfully."}


# Endpoint 3: Serve static HTML file
@app.get("/static-html")
def serve_static_html():
    return {"message": "Static HTML file can be accessed at /static/<filename>.html"}
