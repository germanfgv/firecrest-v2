# FirecREST v2

FirecREST provides a REST API through which developers can interact with HPC resources (Schedulers, Filesystems, etc.). In addition FirecREST provides methods to authenticate and authorize, execution of  jobs through, file-system operations, and access to accounting or status information.


# Running FirecREST v2

To simplify running FirecREST locally we provide a set of local Docker environments that already contain all required dependencies. Please make sure [Docker](https://www.docker.com/) is installed and running on your machine.


To start a local Firecrest environment in VS Code right click the selected environment (e.g."docker-compose-minimal-env.yml") and select "Compose up"

Alternatively, use the command line:
```console
docker-compose -f docker-compose-minimal-env.yml up
```
## Local Environments

### minimal-env
This environment comes with an identity provider (Keycloack) for authentication and a dummy hpc cluster (local Slurm).

The Firecrest endpoints are accessible at: http://localhost:8000/
The Firecrest API swagger: http://localhost:8000/docs

Firecrest connects to the dummy hpc cluster using a static pair of private/public keys.

```credentials
private:
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACCTmVpBD4VS7EO6RyNPQO11PGF2FBtMdDjA1Iwuqe5UhgAAAJBOJ9RhTifU
YQAAAAtzc2gtZWQyNTUxOQAAACCTmVpBD4VS7EO6RyNPQO11PGF2FBtMdDjA1Iwuqe5Uhg
AAAEBg4tXpOBlCkwr9e3RNOgz/e78Gs82oTb6J+OMkxajSSZOZWkEPhVLsQ7pHI09A7XU8
YXYUG0x0OMDUjC6p7lSGAAAAC2FsZUByb3F1ZXJhAQI=
-----END OPENSSH PRIVATE KEY-----

public:
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJOZWkEPhVLsQ7pHI09A7XU8YXYUG0x0OMDUjC6p7lSG ca@cluster
```


## Accessing Firecrest

To access most of the end-points you need an authorization token. Firecrest authorization is based on the standard [Oauth2 Client Credentials Flow](https://auth0.com/docs/get-started/authentication-and-authorization-flow/client-credentials-flow)


All local environments come with pre-configured test credentials:

```credentials
client: firecrest-test-client
secret: wZVHVIEd9dkJDh9hMKc6DTvkqXxnDttk
```

To optain an access token you can either use the Authorize button in the [swagger documentation](http://localhost:8000/docs) or directly access Keycloack's Oauth2 token end-point:  http://localhost:8080/auth/realms/kcrealm/protocol/openid-connect/token


# Development

The repository comes with VS Code settings (.vscode) to facilitate running and debugging a local instance of FirecREST v2.
All necessary VS Code extensions will be listed as recommended and are defined in .vscode/extensions.json.

## Set-up Python Virtual environement

Install python3.12 on your machine.

Create a virtual environment:
```console
python3.12 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-testing.txt
```

Re-lauch VS Code, the virtual env should automatically be enabled on restart.

#### Advanced

To update the local dependencies:
```console
python3 -m pip install -r requirements.txt
```

## Running Tests
From the FirecREST root folder run pytest to execute all unit tests.
```console
source .venv/bin/activate
pip install -r ./requirements.txt -r ./requirements-testing.txt
pytest
```


## Debugging FirecREST v2

The project comes with preconfigured VS Code "Run and Debug" configurations.
The configuration includes proper path mapping to enable breakpoints.

In the VS Code "Run and Debug" tab, select Firecrest API [Docker Compose] hit the play button.


## Accessing Support Services

The Docker environments also include third-party services required by Firecrest to run.

### Keycloak

To access Keycloak’s admin console, navigate to: http://localhost:8080/auth/admin with user-name:admin and password:admin2

Retrieve JWT keys to be used by Slurm for token verification: http://localhost:8080/auth/realms/kcrealm/protocol/openid-connect/certs

Slurm and Firecrest requires the JWT token to inclue the following fields:
- iat: Unix timestamp of creation date.
- exp: Unix timestamp of expiration date.
- username: Slurm UserName ( POSIX.1-2017 User Name ).

Keycloak will set the preffered_username as the Service Accout User associated with the client credentials used to create the token.
To add the username claim to the token:

- Create a Client Scope (e.g. firecrest_v2) with a Mapper. The mapper should add a token claim with name 'username' mapping the user attribute 'scheduler_user'
- To each Firecrest client add the newly created client scope.
- To each Firecrest client service account add the scheduler_user attribute with the value being the scheduler user to impersonate.


### Slurm Dummy Cluster

To ssh into the Slurm Dummy Cluster you can use the fireuser

```console

ssh-keygen -p -s build/environment/keys/fireuser-key -n fireuser -I fireuser -f user-key-cert.pub build/environment/keys/fireuser.pub
chmod 0400 build/environment/keys/fireuser.pub
ssh -i build/environment/keys/fireuser.pub fireuser@localhost -p 2222

```


