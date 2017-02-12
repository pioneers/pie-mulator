from robot import *
from camera import *

class Screen:
    """A visual representation of the field and menu"""


    def __init__(self, robot, gamepad, size):
        self.SCREEN_HEIGHT = size
        self.SCREEN_WIDTH = size
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
        k = self.SCREEN_HEIGHT / 144.0  # screen scaling coefficient
        # print (self.robot.X*k)
        for y in reversed(range(int(self.SCREEN_HEIGHT))):
            line = ["."] * int(self.SCREEN_WIDTH)
            for x in range(int(self.SCREEN_WIDTH)):
                if ((self.robot.X * k) // 1 == x and (self.robot.Y * k) // 1 == y):
                    line[x] = self.symbol()
            print(' '.join(line))
        print("__" * int(self.SCREEN_WIDTH))
        print("X: %s, Y: %s, Theta: %s" % (self.robot.X, self.robot.Y, self.robot.dir))
