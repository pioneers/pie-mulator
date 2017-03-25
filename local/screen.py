class Camera:
    """Create images of parts of the robot in a select format"""
    JOYSTICK_NEUTRAL = "Neutral"
    wheel_base = list("* - - - *|       ||   x   ||       |* - - - *")
    width = 9
    base = list(" " * (5 * width))

    def __init__(self, robot, gamepad):
        self.robot = robot
        self.gamepad = gamepad

    def direction(theta, label='*'):
        """Generate a string that indicates pointing in a theta direction"""
        result = Camera.base.copy()
        result[2 * Camera.width + 4] = label
        if theta == Camera.JOYSTICK_NEUTRAL:
            return Camera.str_format(result)

        theta %= 360
        state = (round(theta / 45.0)) % 8

        result[2 * Camera.width + 4] = label

        if state == 0:
            result[2 * Camera.width + 5] = "-"
            result[2 * Camera.width + 6] = "-"
            result[2 * Camera.width + 7] = "-"
        elif state == 1:
            result[0 * Camera.width + 8] = "/"
            result[1 * Camera.width + 6] = "/"
        elif state == 2:
            result[0 * Camera.width + 4] = "|"
            result[1 * Camera.width + 4] = "|"
        elif state == 3:
            result[0 * Camera.width + 0] = "\\"
            result[1 * Camera.width + 2] = "\\"
        elif state == 4:
            result[2 * Camera.width + 0] = "-"
            result[2 * Camera.width + 1] = "-"
            result[2 * Camera.width + 2] = "-"
        elif state == 5:
            result[3 * Camera.width + 2] = "/"
            result[4 * Camera.width + 0] = "/"
        elif state == 6:
            result[3 * Camera.width + 4] = "|"
            result[4 * Camera.width + 4] = "|"
        elif state == 7:
            result[3 * Camera.width + 6] = "\\"
            result[4 * Camera.width + 8] = "\\"

        return Camera.str_format(result)

    def robot_direction(self):
        """Return a list of strings picturing the direction the robot is traveling in from an overhead view"""
        return Camera.direction(self.robot.dir, Robot.symbol)

    def left_joystick(self):
        """Return a list of strings picturing the left joystick of the gamepad"""
        return Camera.direction(self.gamepad.ltheta(), 'L')

    def right_joystick(self):
        """Return a list of strings picturing the right joystick of the gamepad"""
        return Camera.direction(self.gamepad.rtheta(), 'R')

    def wheel(theta, label='*'):
        """Generate a string picturing a wheel at position theta

        Args:
            theta (float): the angular displacement of the wheel
        """

        result = Camera.wheel_base.copy()
        result[2 * Camera.width + 4] = label
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
        return Camera.wheel(self.robot.rtheta, 'R')

    def left_wheel(self):
        """Return a list of strings picturing the left wheel"""
        return Camera.wheel(self.robot.ltheta, 'L')

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

    SCREEN_HEIGHT = 36
    SCREEN_WIDTH = 36

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
                pre_segment.append(parts_list[x][y] + '  ')
            line_str = ''.join(pre_segment)
            result.append(line_str)
        return result

    def menu_bar(self):
        """Print out the menubar."""
        menu_bar_items = []
        menu_bar_items.append(self.camera.left_wheel())
        menu_bar_items.append(self.camera.right_wheel())
        menu_bar_items.append(self.camera.left_joystick())
        menu_bar_items.append(self.camera.right_joystick())
        Camera.printer(Screen.combiner(menu_bar_items))

    def clear_screen():
        """Clear the previously drawn field"""
        for x in range(40):
            print()

    def symbol(self):
        """Returns a symbol that indicates the robots direction"""
        robot_theta = self.robot.dir
        index = round(robot_theta / 45) % 8
        symbols = ['\u2192', '\u2197', '\u2191', '\u2196', '\u2190', '\u2199', '\u2193', '\u2198']
        return symbols[index]

    def draw(self):
        """Draw the screen."""
        Screen.clear_screen()
        self.menu_bar()
        ky = self.SCREEN_HEIGHT / 144.0  # screen scaling coefficient
        kx = self.SCREEN_WIDTH / 144.0  # screen scaling coefficient
        # print (self.robot.X*k)
        for y in reversed(range(int(self.SCREEN_HEIGHT))):
            line = ["."] * int(self.SCREEN_WIDTH)
            for x in range(int(self.SCREEN_WIDTH)):
                if ((self.robot.X * kx) // 1 == x and (self.robot.Y * ky) // 1 == y):
                    line[x] = self.symbol()
            print(' '.join(line))
        print("__" * int(self.SCREEN_WIDTH))
        print("X: %s, Y: %s, Theta: %s" % (self.robot.X, self.robot.Y, self.robot.dir))
