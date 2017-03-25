import signal
import inspect
import asyncio
import os
from robot import Robot
from screen import Screen
from gamepad import Gamepad
from action import Actions


TIMEOUT_VALUE = 1 # seconds?

Robot = Robot()
Gamepad = Gamepad()
Actions = Actions(Robot)
s = Screen(Robot, Gamepad)

class Simulator:
    @staticmethod
    def simulate(setup_fn=None, loop_fn=None):
        def timeout_handler(signum, frame):
            raise TimeoutError("studentCode timed out")
        signal.signal(signal.SIGALRM, timeout_handler)

        # Need to pass a value by reference, so use a list as a kind of "pointer" cell
        exception_cell = [None]

        clarify_coroutine_warnings(exception_cell)

        try:
            start_watchdog()
            feed_watchdog()

            if setup_fn is None:
                try:
                    import __main__
                    setup_fn = __main__.setup
                except AttributeError:
                    raise RuntimeError("Student code failed to define `setup`")

            if loop_fn is None:
                try:
                    import __main__
                    loop_fn = __main__.loop
                except AttributeError:
                    raise RuntimeError("Student code failed to define `loop`")

            ensure_is_function("setup", setup_fn)
            ensure_is_function("loop", loop_fn)

            feed_watchdog()

            # Note that this implementation does not attempt to re-start student
            # code on failure

            setup_fn()
            feed_watchdog()

            # Now time to start the main event loop
            import asyncio

            async def main_loop():
                while exception_cell[0] is None:
                    next_call = loop.time() + Robot.tick_rate # run at 20 Hz
                    loop_fn()
                    feed_watchdog()

                    # Simulator drawing operation
                    Robot.update()
                    s.draw()

                    sleep_time = max(next_call - loop.time(), 0.)
                    await asyncio.sleep(sleep_time)

                raise exception_cell[0]

            loop = asyncio.get_event_loop()

            def my_exception_handler(loop, context):
                if exception_cell[0] is None:
                    exception_cell[0] = context['exception']

            loop.set_exception_handler(my_exception_handler)
            loop.run_until_complete(main_loop())
        except TimeoutError:
            print("ERROR: student code timed out")
            raise
        except:
            print("ERROR: student code terminated due to an exception")
            raise

class TimeoutError(Exception):
    pass

class RuntimeError(Exception):
    pass

def start_watchdog():
    signal.alarm(TIMEOUT_VALUE)

def feed_watchdog():
    signal.alarm(0) # is this redundant?
    signal.alarm(TIMEOUT_VALUE)

def ensure_is_function(tag, val):
    if inspect.iscoroutinefunction(val):
        raise RuntimeError("{} is defined with `async def` instead of `def`".format(tag))
    if not inspect.isfunction(val):
        raise RuntimeError("{} is not a function".format(tag))

def ensure_not_overridden(module, name):
    if hasattr(module, name):
        raise RuntimeError("Student code overrides `{}`, which is part of the API".format(name))

def clarify_coroutine_warnings(exception_cell):
    """
    Python's default error checking will print warnings of the form:
        RuntimeWarning: coroutine '???' was never awaited

    This function will inject an additional clarification message about what
    such a warning means.
    """
    import warnings

    default_showwarning = warnings.showwarning

    def custom_showwarning(message, category, filename, lineno, file=None, line=None):
        default_showwarning(message, category, filename, lineno, line)

        if str(message).endswith('was never awaited'):
            coro_name = str(message).split("'")[-2]

            print("""
The PiE API has upgraded the above RuntimeWarning to a runtime error!

This error typically occurs in one of the following cases:

1. Calling `Actions.sleep` or anything in `Actions` without using `await`.

Incorrect code:
    async def my_coro():
        Actions.sleep(1.0)

Consider instead:
    async def my_coro():
        await Actions.sleep(1.0)

2. Calling an `async def` function from inside `setup` or `loop` without using
`Robot.run`.

Incorrect code:
    def loop():
        my_coro()

Consider instead:
    def loop():
        Robot.run(my_coro)
""".format(coro_name=coro_name), file=file)
            exception_cell[0] = message

    warnings.showwarning = custom_showwarning
