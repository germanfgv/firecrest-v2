from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, Query


import jwt
from datetime import datetime, timedelta
from typing import Annotated, Any
from jose import jwk, jwt as jwt_jpose
from jose.utils import base64url_encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import yaml
from xmlrpc.client import ServerProxy
from sidecar.config import UnsafeSettings

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


# Endpoint 1: Get token
@app.get("/token")
def get_token(
    username: Annotated[str, Query(description="The username to be added in the JWT")]
):

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

    key = jwk.construct(get_jwk())
    options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}
    decoded_token = jwt_jpose.decode(token=token, key=key, options=options)

    return {"access_token": token, "token_type": "bearer", "decoded": decoded_token}


@app.get("/certs")
def download_certificate():
    return {"keys": [get_jwk()]}


@app.get("/boot")
def boot():

    settings = UnsafeSettings()

    # TODO: inject demo's user settings

    dump: dict[str, Any] = settings.model_dump()
    settings_file = os.getenv("YAML_CONFIG_FILE", None)
    with open(settings_file, "w") as yaml_file:
        yaml.dump(dump, yaml_file)

    # TODO: strat supervisord proc: https://gist.github.com/jalp/10016188

    server = ServerProxy("http://localhost:9001/RPC2")
    server.supervisor.startProcess("firecrest")

    return {"message": "Settings saved successfully."}


# Endpoint 3: Serve static HTML file
@app.get("/static-html")
def serve_static_html():
    return {"message": "Static HTML file can be accessed at /static/<filename>.html"}
