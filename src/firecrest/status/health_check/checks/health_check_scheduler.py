from firecrest.config import ClusterNodesHealth, HPCCluster, SchedulerServiceHealth
from firecrest.dependencies import SchedulerClientDependency
from firecrest.status.health_check.checks.health_check_base import HealthCheckBase


class SchedulerHealthCheck(HealthCheckBase):

    def __init__(self, auth, token, system: HPCCluster, timeout: int):
        super().__init__(system)
        self.auth = auth
        self.token = token
        self.timeout = timeout

    async def execute_check(self) -> SchedulerServiceHealth:

        self.scheduler_client = await SchedulerClientDependency(ignore_health=True)(
            system_name=self.system.name
        )

        health = SchedulerServiceHealth(service_type="scheduler")
        health.healthy = True
        available, total = await self.scheduler_client.health_check(
            self.auth.username, self.token["access_token"], timeout=self.timeout
        )
        health.nodes = ClusterNodesHealth(available=available, total=total)

        return health

    async def handle_error(self, ex: Exception) -> SchedulerServiceHealth:
        error_message = f"{ex.__class__.__name__}"
        if len(str(ex)) > 0:
            error_message = f"{ex.__class__.__name__}: {str(ex)}"
        health = SchedulerServiceHealth(service_type="scheduler")
        health.healthy = False
        health.message = error_message
        return health
