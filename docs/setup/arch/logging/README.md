# FirecREST logging

FirecREST utilizes [Uvicorn](https://www.uvicorn.org/) as HTTP server and it can be configured to accept different types of loggers and formatters using the [UVICORN_LOG_CONFIG](https://www.uvicorn.org/settings/#logging) file.

This file is based in the Python3 [logging configuration](https://docs.python.org/3/library/logging.config.html#object-connections) YAML format, and must be included as a FirecREST environment variable (ie, `UVICORN_LOG_CONFIG: /app/config/log-conf.yaml`) along with the set to `true` of the `logger.enable_tracing_log` configuration variable.

## Logging config file

Sysadmins can use the following file as a starting point to configure the FirecREST deployment:

!!! example "Logging config file example"
    ```yaml
    version: 1
    disable_existing_loggers: False
    formatters:
    default:
        # "()": uvicorn.logging.DefaultFormatter
        format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    access:
        # "()": uvicorn.logging.AccessFormatter
        format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    jsonformatter:
        format: '%(asctime)s %(levelname)s %(name)s %(message)s'
        class: pythonjsonlogger.jsonlogger.JsonFormatter
    handlers:
    default:
        formatter: default
        class: logging.StreamHandler
        stream: ext://sys.stderr
    access:
        formatter: access
        class: logging.StreamHandler
        stream: ext://sys.stdout
    json_handler:
        formatter: jsonformatter
        class: logging.StreamHandler
        stream: ext://sys.stdout
    loggers:
    uvicorn.error:
        level: INFO
        handlers:
        - default
        propagate: no
    uvicorn.access:
        level: INFO
        handlers:
        - access
        propagate: no
    f7t_v2_tracing_log:
        level: INFO
        handlers:
        - json_handler
        propagate: no
    root:
    level: ERROR
    handlers:
        - default
    propagate: no
    ```

## Log formats

The format of the logs is defined in the `f7t_v2_tracing_log` tracer and currently allows the following formats:

### Format for HTTP backend

When the backend service that FirecREST is interfacing (for instance, [SLURM RESTd](https://slurm.schedmd.com/slurmrestd.html) abstraction), the format includes in the `backend` field the queried `url` and the HTTP `response_status` of the HTTP response.

!!! example "FirecREST Log format for HTTP backend"

    ```json
    {
        "asctime": "2025-04-15 16:51:57,598",
        "levelname": "INFO",
        "name": "f7t_v2_tracing_log",
        "message": "",
        "username": "fireuser",
        "system_name": "cluster-slurm-api",
        "endpoint": "/status/cluster-slurm-api/partitions",
        "resource": "status",
        "status_code": 200,
        "user_agent": "PostmanRuntime/7.43.2",
        "backend": {
            "url": "http://192.168.240.2:6820/slurm/v0.0.42/partitions",
            "response_status": "200"
        }
    }
    ```

#### Log output examples

??? example "Sample output for JSON formatter `pythonjsonlogger.jsonlogger.JsonFormatter`"
    ```text
    firecrest-1             | {"asctime": "2025-04-15 16:46:09,900", "levelname": "INFO", "name": "f7t_v2_tracing_log", "message": "", "username": "fireuser", "endpoint": "/status/systems", "resource": "status", "status_code": 200, "user_agent": "PostmanRuntime/7.43.2"}
    firecrest-1             | {"asctime": "2025-04-15 16:47:06,075", "levelname": "INFO", "name": "f7t_v2_tracing_log", "message": "", "username": "fireuser", "system_name": "cluster", "endpoint": "/status/cluster/partitions", "resource": "status", "status_code": 404, "user_agent": "PostmanRuntime/7.43.2"}
    firecrest-1             | {"asctime": "2025-04-15 16:51:20,278", "levelname": "INFO", "name": "f7t_v2_tracing_log", "message": "", "username": "fireuser", "system_name": "cluster", "endpoint": "/status/cluster/userinfo", "resource": "status", "status_code": 404, "user_agent": "PostmanRuntime/7.43.2"}
    firecrest-1             | {"asctime": "2025-04-15 16:51:57,598", "levelname": "INFO", "name": "f7t_v2_tracing_log", "message": "", "username": "fireuser", "system_name": "cluster-slurm-api", "endpoint": "/status/cluster-slurm-api/partitions", "resource": "status", "status_code": 200, "user_agent": "PostmanRuntime/7.43.2", "backend": {"url": "http://192.168.240.2:6820/slurm/v0.0.42/partitions", "response_status": "200"}}
    firecrest-1             | {"asctime": "2025-04-15 16:52:19,457", "levelname": "INFO", "name": "f7t_v2_tracing_log", "message": "", "username": "fireuser", "system_name": "cluster-slurm-cli", "endpoint": "/status/cluster-slurm-cli/partitions", "resource": "status", "status_code": 404, "user_agent": "PostmanRuntime/7.43.2"}
    firecrest-1             | {"asctime": "2025-04-15 16:52:25,506", "levelname": "INFO", "name": "f7t_v2_tracing_log", "message": "", "username": "fireuser", "system_name": "cluster-slurm-ssh", "endpoint": "/status/cluster-slurm-ssh/partitions", "resource": "status", "status_code": 200, "user_agent": "PostmanRuntime/7.43.2", "backend": {"command": "scontrol -a show -o partitions", "exit_status": "0"}}    
    ```


### Format for SSH backend

On the other hand, if FirecREST is executing a command via an SSH command execution, the `backend` field provides the actual `command` to be executed, and the POSIX `exit_status` of the command.

!!! example "FirecREST Log format for SSH backend"
    ```json
    {
        "asctime": "2025-04-15 16:52:25,506",
        "levelname": "INFO",
        "name": "f7t_v2_tracing_log",
        "message": "",
        "username": "fireuser",
        "system_name": "cluster-slurm-ssh",
        "endpoint": "/status/cluster-slurm-ssh/partitions",
        "resource": "status",
        "status_code": 200,
        "user_agent": "PostmanRuntime/7.43.2",
        "backend": {
            "command": "scontrol -a show -o partitions",
            "exit_status": "0"
        }
    }
    ```

#### Log output examples

??? example "Sample output for Default formatter"
    ```text
    2025-04-15 16:57:20,908 - f7t_v2_tracing_log - INFO - {'username': 'fireuser', 'system_name': 'cluster-slurm-ssh', 'endpoint': '/status/cluster-slurm-ssh/partitions', 'resource': 'status', 'status_code': 200, 'user_agent': 'PostmanRuntime/7.43.2', 'backend': {'command': 'scontrol -a show -o partitions', 'exit_status': '0'}}
    2025-04-15 16:59:46,478 - f7t_v2_tracing_log - INFO - {'username': 'fireuser', 'system_name': 'cluster-slurm-ss', 'endpoint': '/status/cluster-slurm-ss/partitions', 'resource': 'status', 'status_code': 404, 'user_agent': 'PostmanRuntime/7.43.2'}
    2025-04-15 16:59:57,159 - f7t_v2_tracing_log - INFO - {'username': 'fireuser', 'system_name': 'cluster-slurm-ssh', 'endpoint': '/status/cluster-slurm-ssh/nodes', 'resource': 'status', 'status_code': 200, 'user_agent': 'PostmanRuntime/7.43.2', 'backend': {'command': "sinfo -N --noheader --format='%z|%c|%O|%e|%f|%N|%o|%n|%T|%R|%w|%v|%m|%C'", 'exit_status': '0'}}
    ```
