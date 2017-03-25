import signal
import inspect
import asyncio
import os
import math

class Robot:
    """The MODEL for this simulator. Stores robot data and handles position
       calculations & Runtime API calls """
    tick_rate = 0.05             # in s
    width = 12                  # width of robot , inches
    w_radius = 2                # radius of a wheel, inches
    MAX_X = 143                 # maximum X value, inches, field is 12'x12'
    MAX_Y = 143                 # maximum Y value, inches, field is 12'x12'
    neg = -1                    # negate left motor calculation
    symbol = '@'                # the character representation of the robot on the field

    def __init__(self):
        self.X = 72.0           # X position of the robot
        self.Y = 72.0           # Y position of the robot
        self.Wl = 0.0           # angular velocity of l wheel, degree/s
        self.Wr = 0.0           # angular velocity of r wheel, degree/s
        self.ltheta = 0.0       # angular position of l wheel, degree
        self.rtheta = 0.0       # angular position of r wheel, degree
        self.dir = 0.0         # Direction of the robot facing, degree

        self._coroutines_running = set()

    """ Differential Drive Calculation Reference:
    https://chess.eecs.berkeley.edu/eecs149/documentation/differentialDrive.pdf
    """
    def update(self):
        """Updates position of the  Robot using differential drive equations"""
        lv = self.Wl * Robot.w_radius * Robot.neg
        rv = self.Wr * Robot.w_radius
        radian = math.radians(self.dir)
        if (lv == rv):
            distance = rv * Robot.tick_rate
            dx = distance * math.cos(radian)
            dy = distance * math.sin(radian)

        else:
            rt = Robot.width/2 * (lv+rv)/(rv-lv)
            Wt = (rv-lv)/Robot.width
            theta = Wt * Robot.tick_rate
            i = rt * (1 - math.cos(theta))
            j = math.sin(theta) * rt
            dx = i * math.sin(radian) + j * math.cos(radian)
            dy = i * math.cos(radian) + j * math.sin(radian)
            self.dir = (self.dir + math.degrees(theta)) % 360
        self.X = max(min(self.X + dx, Robot.MAX_X), 0)
        self.Y = max(min(self.Y + dy, Robot.MAX_Y), 0)
        self.ltheta = (self.Wl * 5 + self.ltheta) % 360
        self.rtheta = (self.Wr * 5 + self.rtheta) % 360

    def set_value(self, device, speed):
        """Runtime API method for updating L/R motor speed. Takes only L/R
           Motor as device name and speed bounded by [-1,1]."""
        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed cannot be great than 1.0 or less than -1.0.")
        if device == "left_motor":
            self.Wl = speed * 9
        elif device == "right_motor":
            self.Wr = speed * 9
        else:
            raise KeyError("Cannot find device name: " + device)

    def run(self, fn, *args, **kwargs):
        """
        Starts a "coroutine", i.e. a series of actions that proceed
        independently of the main loop of code.

        The first argument must be a function defined with `async def`.

        The remaining arguments are then passed to that function before it is
        called.

        Multiple simultaneous coroutines that use the same robot actuators will
        lead to surprising behavior. To help guard against errors, calling
        `Robot.run` with a `fn` argument that is currently running is a no-op.
        """

        if not inspect.isfunction(fn):
            raise ValueError("First argument to Robot.run must be a function")
        elif not inspect.iscoroutinefunction(fn):
            raise ValueError("First argument to Robot.run must be defined with `async def`, not `def`")

        if fn in self._coroutines_running:
            return

        self._coroutines_running.add(fn)

        future = fn(*args, **kwargs)

        async def wrapped_future():
            await future
            self._coroutines_running.remove(fn)

        # asyncio.ensure_future(wrapped_future())
        asyncio.ensure_future(wrapped_future())

    def is_running(self, fn):
        """
        Returns True if the given `fn` is already running as a coroutine.

        See: Robot.run
        """

        if not inspect.isfunction(fn):
            raise ValueError("First argument to Robot.is_running must be a function")
        elif not inspect.iscoroutinefunction(fn):
            raise ValueError("First argument to Robot.is_running must be defined with `async def`, not `def`")

        return fn in self._coroutines_running
