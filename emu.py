"""
Goals for view:
    Display a field
    Display the robot on the field
    Display the mnu
        Display the motors
        Display the robot orientation
"""


class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Wheel:

    base = list("*---*|   || x ||   |*___*")

    def img(theta):
        """Returns a list of the component strings based on angle"""
        result = Wheel.base.copy()
        state = round(theta / 45.0) % 8

        assert state != 8

        if state == 0:
            result[1 * 5 + 2] = "|"
        elif state == 1:
            result[1 * 5 + 3] = "/"
        elif state == 2:
            result[2 * 5 + 3] = "-"
        elif state == 3:
            result[3 * 5 + 3] = "\\"
        elif state == 4:
            result[3 * 5 + 2] = "|"
        elif state == 5:
            result[3 * 5 + 1] = "/"
        elif state == 6:
            result[2 * 5 + 1] = "-"
        elif state == 7:
            result[1 * 5 + 1] = "\\"
        return result

    def printer(listy):
        for y in range(5):
            segment = listy[y * 5:(y + 1) * 5]
            print(''.join(segment))

class MenuBar:
    """Contains  mostly nongraphic stats"""

    def __init__(self, robot):
        self.robot = robot

    def robot_direction(theta):
        [

        if t



class Screen:
    """A visual representation of the field and menu"""
    SCREEN_HEIGHT = 25
    SCREEN_WIDTH = 25

    def __init__(self, robot):
        self.robot = robot

    def draw(self):
        for y in range(Screen.SCREEN_HEIGHT):
            line = ["."] * 50
            for x in range(Screen.SCREEN_WIDTH):
                if (self.robot.x // 1 == x and self.robot.y // 1 == y):
                    line[x] = "@"
            print(''.join(line))

if __name__ == "__main__":
    r = Robot(12, 12)
    s = Screen(r)
    s.draw()
