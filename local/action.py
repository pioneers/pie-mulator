import signal
import inspect
import asyncio
import os

def _ensure_strict_semantics(fn):
    """
    (Internal): provides additional error checking for the PiE API
    """
    if not inspect.iscoroutinefunction(fn):
        raise Exception("Internal runtime error: _ensure_strict_semantics can only be applied to `async def` functions")

    def wrapped_fn(*args, **kwargs):
        # Ensure that this function is called directly out of the event loop,
        # and not out of the `setup` and `loop` functions.
        stack = inspect.stack()
        try:
            for frame in stack:
                if os.path.basename(frame.filename) == "base_events.py" and frame.function == "_run_once":
                    # We've hit the event loop, so everything is good
                    break
                elif os.path.basename(frame.filename) == "pimulator.py" and frame.function == 'simulate':
                    # We've hit the runtime before hitting the event loop, which
                    # is bad
                    raise Exception("Call to `{}` must be inside an `async def` function called using `Robot.run`".format(fn.__name__))
        finally:
            del stack
        return fn(*args, **kwargs)

    return wrapped_fn
    
class Actions:
    """
    This class contains a series of pre-specified actions that a robot can
    perform. These actions should be used inside a coroutine using an `await`
    statement, e.g. `await Actions.sleep(1.0)`
    """

    def __init__(self, robot):
        self._robot = robot

    @_ensure_strict_semantics
    async def sleep(self, seconds):
        """
        Waits for specified number of `seconds`
        """

        await asyncio.sleep(seconds)
