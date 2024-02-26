import time
from typing import Any
from typing import Callable
from typing import Optional


def _retry(
    fn: Callable[[], Any],
    fn_args: Optional[list] = None,
    fn_kwargs: Optional[dict] = None,
    timeout: int = 0,
) -> Any:
    """Retry a function until it returns a non-falsey result or timeout is hit.

    If timeout is set to 0, the function will only be run once.

    This will not wrap Exceptions, only falsey values.

    Arguments:
        fn: A function to retry.
        timeout: How long, in seconds, to retry the function.

    Returns:
        The final return value of func.
    """
    fn_args = fn_args or []
    fn_kwargs = fn_kwargs or {}

    result = None

    # Zero second wait time means only check once
    if timeout == 0:
        result = fn(*fn_args, **fn_kwargs)
    else:
        end_time = time.time() + timeout

        while time.time() < end_time:
            result = fn(*fn_args, **fn_kwargs)

            if result:
                break

    return result
