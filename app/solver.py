import asyncio
import logging
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from . import tasks
from .statistics import Statistics

log = logging.getLogger(__name__)


class SolverTaskTimeout(Exception):
    pass


class Solver:
    def __init__(self, max_workers, timeout):
        self._process_pool = multiprocessing.Pool(processes=max_workers)
        self.timeout = timeout

    async def _submit(self, task, timeout, *args, **kwargs):
        loop = asyncio.get_running_loop()
        async_result = self._process_pool.apply_async(
            task, args=args, kwds=kwargs
        )

        try:
            result = await loop.run_in_executor(
                None,
                async_result.get, timeout or self.timeout
            )
        except multiprocessing.TimeoutError:
            log.error(
                'Timeout %s for task ask %s with args %s kwargs %s',
                self.timeout, task.__name__, args, kwargs
            )
            raise SolverTaskTimeout
        except Exception as exc:
            log.error(exc)
        else:
            return result

    @Statistics.gather
    async def ackermann(self, *, m, n, timeout=None):
        result = await self._submit(tasks.ackermann_nonrec, timeout, m=m, n=n)
        return result

    @Statistics.gather
    async def factorial(self, *, n, timeout=None):
        result = await self._submit(tasks.factorial, timeout, n=n)
        return result

    @Statistics.gather
    async def fibonacci(self, *, n, timeout=None):
        result = await self._submit(tasks.fibonacci, timeout, n=n)
        return result
