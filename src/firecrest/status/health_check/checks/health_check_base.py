from abc import ABC, abstractmethod
import time

from firecrest.config import BaseServiceHealth, HPCCluster


class HealthCheckBase(ABC):

    def __init__(self, system: HPCCluster):
        self.system = system

    async def check(self) -> BaseServiceHealth:
        health: BaseServiceHealth
        start_time = time.time()
        try:
            health = await self.execute_check()
            health.healthy = True
        except Exception as ex:
            health = await self.handle_error(ex)

        health.last_checked = time.time()
        health.latency = time.time() - start_time

        return health

    @abstractmethod
    async def execute_check(self) -> BaseServiceHealth:
        pass

    @abstractmethod
    async def handle_error(self, ex: Exception) -> BaseServiceHealth:
        pass
