from typing import Any
import time
from datetime import datetime
from dataclasses import dataclass

from . import solver


class Statistics:

    @dataclass
    class Item:
        func_name: str
        created: datetime
        execution_time: float
        args: tuple
        kwargs: dict
        result: Any

    data = {}

    @classmethod
    def gather(cls, func):
        async def wrapper(*args, **kwargs):
            result = None
            start = time.monotonic()
            try:
                result = await func(*args, **kwargs)
            except solver.SolverTaskTimeout:
                result = 'TimeoutError'
                raise
            except Exception:
                raise
            finally:
                execution_time = time.monotonic() - start
                now = datetime.utcnow()
                stats_item = Statistics.Item(
                    func_name=func.__name__,
                    created=now,
                    execution_time=execution_time,
                    args=args,
                    kwargs=kwargs,
                    result=result,
                )
                cls.data[(now, func.__name__)] = stats_item
            return result
        return wrapper
