import time
from typing import Any, Callable, Optional


def _retry(
    fn: Callable[[], Any],
    fn_args: Optional[list] = None,
    fn_kwargs: Optional[dict] = None,
    timeout: int = 0,
) -> bool:
    """Retry a function that should return a truthy value until a timeout is hit.

    Arguments:
        fn: Function to retry
        timeout: Number of seconds to retry.

    Returns:
        bool - True if the function returns a truthy value before the timeout, else False.

    """
    fn_args = fn_args or []
    fn_kwargs = fn_kwargs or {}

    end_time = time.time() + timeout

    while time.time() < end_time:
        result = fn(*fn_args, **fn_kwargs)
        if result:
            return True
    return False
