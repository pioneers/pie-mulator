import math
import time
from gamepad import *


class Robot:
    """The MODEL for this simulator. Stores robot data and handles position
       calculations & Runtime API calls """
    tick_rate = 0.1             # in s
    width = 12                  # width of robot , inches
    w_radius = 2                # radius of a wheel, inches
    MAX_X = 143                 # maximum X value, inches, field is 12'x12'
    MAX_Y = 143                 # maximum Y value, inches, field is 12'x12'
    neg = -1                    # negate left motor calculation

    def __init__(self):
        self.X = 72.0           # X position of the robot
        self.Y = 72.0           # Y position of the robot
        self.Wl = 0.0           # angular velocity of l wheel, degree/s
        self.Wr = 0.0           # angular velocity of r wheel, degree/s
        self.ltheta = 0.0       # angular position of l wheel, degree
        self.rtheta = 0.0       # angular position of r wheel, degree
        self.dir = 90.0         # Direction of the robot facing, degree

    """ Differential Drive Calculation Reference:
    https://chess.eecs.berkeley.edu/eecs149/documentation/differentialDrive.pdf
    """
    def update_position(self):
        """Updates position of the  Robot using differential drive equations"""
        lv = self.Wl * Robot.w_radius * Robot.neg
        rv = self.Wr * Robot.w_radius
        radian = math.radians(self.dir)
        if (lv == rv):
            distance = rv * Robot.tick_rate
            dx = distance * math.cos(radian)
            dy = distance * math.sin(radian)
            print(dx)
            print(dy)
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


class Camera:
    """Create images of parts of the robot in a select format"""
    JOYSTICK_NEUTRAL = "Neutral"
    wheel_base = list("* - - - *|       ||   x   ||       |* - - - *")
    width = 9
    base = list(" " * (5 * width))

    def __init__(self, robot, gamepad):
        self.robot = robot
        self.gamepad = gamepad

    def direction(theta):
        """Generate a string that indicates pointing in a theta direction"""
        if theta == Camera.JOYSTICK_NEUTRAL:
            return Camera.base

        theta %= 360
        result = Camera.base.copy()
        state = (round(theta / 45.0) - 2) % 8

        result[2 * Camera.width + 4] = "*"

        if state == 0:
            result[0 * Camera.width + 4] = "|"
            result[1 * Camera.width + 4] = "|"
        elif state == 1:
            result[0 * Camera.width + 8] = "/"
            result[1 * Camera.width + 6] = "/"
        elif state == 2:
            result[2 * Camera.width + 5] = "-"
            result[2 * Camera.width + 6] = "-"
            result[2 * Camera.width + 7] = "-"
        elif state == 3:
            result[3 * Camera.width + 6] = "\\"
            result[4 * Camera.width + 8] = "\\"
        elif state == 4:
            result[3 * Camera.width + 4] = "|"
            result[4 * Camera.width + 4] = "|"
        elif state == 5:
            result[3 * Camera.width + 2] = "/"
            result[4 * Camera.width + 0] = "/"
        elif state == 6:
            result[2 * Camera.width + 0] = "-"
            result[2 * Camera.width + 1] = "-"
            result[2 * Camera.width + 2] = "-"
        elif state == 7:
            result[0 * Camera.width + 0] = "\\"
            result[1 * Camera.width + 2] = "\\"
        return Camera.str_format(result)

    def robot_direction(self):
        """Return a list of strings picturing the direction the robot is traveling in from an overhead view"""
        return Camera.direction(self.robot.dir)

    def left_joystick(self):
        """Return a list of strings picturing the left joystick of the gamepad"""
        return Camera.direction(self.gamepad.ltheta())

    def right_joystick(self):
        """Return a list of strings picturing the right joystick of the gamepad"""
        return Camera.direction(self.gamepad.rtheta())

    def wheel(theta):
        """Generate a string picturing a wheel at position theta

        Args:
            theta (float): the angular displacement of the wheel
        """

        result = Camera.wheel_base.copy()
        state = round(theta / 45.0) % 8

        if state == 0:
            result[1 * Camera.width + 4] = "|"
        elif state == 2:
            result[1 * Camera.width + 7] = "/"
        elif state == 2:
            result[2 * Camera.width + 7] = "-"
        elif state == 3:
            result[3 * Camera.width + 7] = "\\"
        elif state == 4:
            result[3 * Camera.width + 4] = "|"
        elif state == 5:
            result[3 * Camera.width + 1] = "/"
        elif state == 6:
            result[2 * Camera.width + 1] = "-"
        elif state == 7:
            result[1 * Camera.width + 1] = "\\"

        return Camera.str_format(result)

    def right_wheel(self):
        """Return a list of strings picturing the right wheel"""
        return Camera.wheel(self.robot.rtheta)

    def left_wheel(self):
        """Return a list of strings picturing the left wheel"""
        return Camera.wheel(self.robot.ltheta)

    def str_format(list_img):
        """Return a list of 5 strings each of length 9

        Args:
            list_img: A list of 5 * 9 characters
        """
        result = []
        for y in range(5):
            segment = list_img[y * Camera.width:(y + 1) * Camera.width]
            result.append(''.join(segment))
        return result

    def printer(formatted_list):
        """Print a list of strings to graphically resemble it"""
        for x in formatted_list:
            print(x)


class Screen:
    """A visual representation of the field and menu"""

    SCREEN_HEIGHT = 48
    SCREEN_WIDTH = 48

    def __init__(self, robot, gamepad):
        self.robot = robot
        self.gamepad = gamepad
        self.camera = Camera(robot, gamepad)

    def combiner(parts_list):
        """Return a list of 5 strings that make up the menu_bar.

        args:
            parts_list: a list where each element is a list of 5 strings picturing an element
        """

        result = []
        for y in range(5):
            pre_segment = []
            for x in range(len(parts_list)):
                pre_segment.append(parts_list[x][y])
            line_str = ''.join(pre_segment)
            result.append(line_str)
        return result

    def menu_bar(self):
        """Print out the menubar."""
        menu_bar_items = []
        menu_bar_items.append(self.camera.right_wheel())
        menu_bar_items.append(self.camera.left_wheel())
        menu_bar_items.append(self.camera.robot_direction())
        menu_bar_items.append(self.camera.left_joystick())
        Camera.printer(Screen.combiner(menu_bar_items))

    def draw(self):
        """Draw the screen."""
        self.menu_bar()
        k = Screen.SCREEN_HEIGHT / 144.0  # screen scaling coefficient
        # print (self.robot.X*k)
        for y in range(int(Screen.SCREEN_HEIGHT)):
            line = ["."] * int(Screen.SCREEN_WIDTH)
            for x in range(int(Screen.SCREEN_WIDTH)):
                if ((self.robot.X * k) // 1 == x and (self.robot.Y * k) // 1 == y):
                    line[x] = "@"
            print(' '.join(line))
        print("__" * int(Screen.SCREEN_WIDTH))

if __name__ == "__main__":
    r = Robot()
    g = Gamepad()
    s = Screen(r, g)

    while True:
        r.set_value("left_motor", 1)
        r.set_value("right_motor", 1)
        g.godmode("left_joystick_x", .3)
        r.update_position()
        s.draw()
        time.sleep(r.tick_rate)
