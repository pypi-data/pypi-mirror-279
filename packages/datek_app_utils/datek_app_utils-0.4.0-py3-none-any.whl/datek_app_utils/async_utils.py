import sys
from asyncio import CancelledError, Task, create_task, gather, sleep
from functools import wraps
from typing import Awaitable, Callable, Optional, TypeVar

if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import ParamSpec
else:  # pragma: no cover
    from typing_extensions import ParamSpec


P = ParamSpec("P")
T = TypeVar("T")


def async_timeout(seconds: float):
    def decorator(func: Callable[P, Awaitable[T]]):
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Awaitable[T]:
            timeout_task: Optional[Task] = None
            main_task: Optional[Task] = None

            async def raise_timeout_error():
                try:
                    await sleep(seconds)
                except CancelledError:
                    return

                if main_task:
                    main_task.cancel()

                raise TimeoutError

            async def main():
                try:
                    return await func(*args, **kwargs)
                except Exception:
                    raise
                finally:
                    if timeout_task:
                        timeout_task.cancel()

            timeout_task = create_task(raise_timeout_error())
            main_task = create_task(main())

            result, _ = await gather(main_task, timeout_task)
            return result

        return wrapper

    return decorator
