import math
import time

class Robot:
    tick_rate = 0.1            #in s
    width = 4                   #width of robot
    w_radius = 0.67                #radius of a wheel
    MAX_X = 47
    MAX_Y = 47
    def __init__ (self):
        self.X = 24.0           #X position of the robot
        self.Y = 24.0           #Y position of the robot
        self.Wl = 0.0           #angular velocity of l wheel, degree/s
        self.Wr = 0.0           #angular velocity of r wheel, degree/s
        self.ltheta = 0.0       #angular position of l wheel, in degree
        self.rtheta = 0.0       #angular position of r wheel, in degree
        self.dir = 45           #Direction of the robot facing,in degree


    def update_position(self):
        self.ltheta = (self.ltheta + self.Wl * Robot.tick_rate)%360
        self.rtheta = (self.rtheta + self.Wr * Robot.tick_rate)%360
        lv = self.Wl * Robot.w_radius
        rv = self.Wr * Robot.w_radius
        rt = Robot.width/2 * (lv+rv)/(rv-lv)
        Wt = (rv-lv)/Robot.width
        theta = Wt* Robot.tick_rate
        i = rt * (1 - math.cos(theta))
        j = math.sin(theta)* rt
        dx = i*math.sin(self.dir) + j*math.cos(self.dir)
        dy = i*math.cos(self.dir) + j*math.sin(self.dir)
        self.X = max(min(self.X + dx, Robot.MAX_X),0)
        self.Y = max(min(self.Y + dy, Robot.MAX_Y),0)
        self.dir = (self.dir + theta)%360

        self.ltheta = (self.Wl * 15+ self.ltheta) % 360
        self.rtheta = (self.Wr * 15+ self.rtheta) % 360

    def set_value(self, device, speed):
        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed cannot be great than 1.0 or less than -1.0.")
        if (device == "left_motor"):
            self.Wl = -speed * 3
        elif device == "right_motor":
            self.Wr = speed * 3
        else:
            raise KeyError("Cannot find device name: " + device)


class Camera:
    wheel_base = list("* - - - *|       ||   x   ||       |* - - - *")
    width = 9
    base = list(" " * (5 * width))

    def __init__(self, robot, gamepad):
        self.robot = robot
        self.gamepad = gamepad

    def direction(theta):
        result = Camera.base.copy()
        state = round(theta / 45.0) % 8

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
        return Camera.direction(self.robot.dir)

    def left_joystick(self):
        return Camera.direction(self.gamepad.ltheta())

    def right_joystick(self):
        return Camera.direction(self.gamepad.rtheta())

    def wheel(theta):
        result = Camera.wheel_base.copy()
        state = round(theta / 45.0) % 8

        if state == 0:
            result[1 * Camera.width + 4] = "|"
        elif state == 1:
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
        return Camera.wheel(self.robot.rtheta)

    def left_wheel(self):
        return Camera.wheel(self.robot.ltheta)

    def str_format(list_img):
        """Returns a list of 5 strings of length 9"""
        result = []
        for y in range(5):
            segment = list_img[y * Camera.width:(y + 1) * Camera.width]
            result.append(''.join(segment))
        return result

    def printer(formatted_list):
        for x in formatted_list:
            print(x)


class Screen:
    """A visual representation of the field and menu"""
    SCREEN_HEIGHT = 48
    SCREEN_WIDTH = 48

    def __init__(self, robot, gamepad):
        self.robot = robot
        self.gamepad = gamepad
        self.camera = Camera(self.robot, self.gamepad)

    def combiner(parts_list):
        result = []
        for y in range(5):
            pre_segment = []
            for x in range(len(parts_list)):
                pre_segment.append(parts_list[x][y])
            line_str = ''.join(pre_segment)
            result.append(line_str)
        return result

    def menu_bar(self):
        menu_bar_items = []
        menu_bar_items.append(self.camera.right_wheel())
        menu_bar_items.append(self.camera.left_wheel())
        menu_bar_items.append(self.camera.robot_direction())
        Camera.printer(Screen.combiner(menu_bar_items))

    def draw(self):
        # print the menu bar
        self.menu_bar()

        # print the map
        for y in reversed(range(Screen.SCREEN_HEIGHT)):
            line = ["."] * Screen.SCREEN_WIDTH
            for x in range(Screen.SCREEN_WIDTH):
                if (self.robot.X // 1 == x and self.robot.Y // 1 == y):
                    line[x] = "@"
            print(' '.join(line))
        print("__" * Screen.SCREEN_WIDTH)

if __name__ == "__main__":
    r = Robot()
    r.set_value("left_motor", 1)
    r.set_value("right_motor", .9)
    s = Screen(r, "place holder for gamepad")

    while True:
        r.update_position()
        s.draw()
        time.sleep(r.tick_rate)

