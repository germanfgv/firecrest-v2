# Web UI with Client Credentials

## Introduction

Example of Web GUI (Graphic User Interface) application on Python (Flask) to interface HCP services using FirecREST.

This example uses Authentication with an IdP (Identity Provider) with the [Client Credential Workflow](https://oauth.net/2/grant-types/client-credentials/).

Follow the Configuration guide to adapt your client credentials to the app.

## Prerequisites

- Docker installed
- Knowledge of Python

## Configuration

1. Copy the configuration file (`src/config.py.orig`) and rename it as `src/config.py`

    !!! example "Copy empty configuration file"
        ```bash
        $ cd src
        $ cp config.py.orig config.py
        ```

2. Replace the follwing values with the specifics for this training 

    !!! example "Complete configuration file"
        ```python
        ...
        class DevConfig(Config)
            OIDC_CLIENT_ID = "<CLIENT_ID>" 
            OIDC_CLIENT_SECRET = "<CLIENT_SECRET>" 
            USER_GROUP="<Unix Group of the User associated with your Client Credential client>"
            OIDC_AUTH_BASE_URL = "<IdP Auth Endpoint>"
            OIDC_AUTH_REALM = "<IdP Auth Realm>"
            FIRECREST_URL="<FirecREST URL>"
            SYSTEM_NAME="<Name of the system to interface>"
        ```

- For **debugging** purposes, leave the default values in the variables `SBATCH_TEMPLATE`, `PROBLEM_INI_FILE`, `PROBLEM_MSH_FILE`, and `POST_TEMPLATE`.
- For **testing a "real"** case, use:
    !!! example "Configuration file: problem setup"
        ```python
        ...
        PROBLEM_INI_FILE = 'inc-cylinder.ini'
        PROBLEM_MSH_FILE = 'inc-cylinder.msh'
        SBATCH_TEMPLATE = "cylinder.sh.tmpl"
        POST_TEMPLATE = "post_proc.sh.tmpl"
        ```

*In this case, you would need to use [Sarus](https://products.cscs.ch/sarus/)*

## Build and run

!!! example "Build app and run"
    ```bash
    make build
    make run
    ```

You can check the logs in `log/client.log`

!!! example "Check the logs"
    ```bash
    $ tail -f log/client.log
    ```

## How does it work for the user

- Open a browser, and enter [http://localhost:9090](http://localhost:9091)
- Set the parameters of the problem (number of steps, nodes, job name, etc)
- Click `Submit Jobs` to run the simulation (you should see the jobs created in the list, and new result files in `Working directory`)
- Click on `Start Postprocessing` to launch a job and after completion see the animated gif result image
