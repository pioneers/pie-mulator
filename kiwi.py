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
        else :
            raise KeyError("Cannot find device name: " + device)

class Wheel:
    base = list("*---*|   || x ||   |*---*")

    def __init__ (self, robot):
        self.robot = robot

    def img(self):
        """Returns a list of the component strings based on angle"""
        theta = self.robot.ltheta

        result = list(Wheel.base)
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

    def printer(self,listy):
        for y in range(5):
            segment = listy[y * 5:(y + 1) * 5]
            print(' '.join(segment))

class MenuBar:
    """Contains  mostly nongraphic stats"""

    def __init__(self, robot):
        self.robot = robot

    def robot_direction(self):
        self.robot.dir
        return


class Screen:
    """A visual representation of the field and menu"""
    SCREEN_HEIGHT = 48
    SCREEN_WIDTH = 48

    def __init__(self, robot):
        self.robot = robot

    def draw(self):
        for y in range(Screen.SCREEN_HEIGHT):
            line = ["."] * Screen.SCREEN_WIDTH
            for x in range(Screen.SCREEN_WIDTH):
                if (self.robot.X // 1 == x and self.robot.Y // 1 == y):
                    line[x] = "@"
            print(' '.join(line))
        print("__"* Screen.SCREEN_WIDTH)

if __name__ == "__main__":
    r = Robot()
    w = Wheel(r)
    s = Screen(r)
    while True:
        r.set_value("left_motor", 1)
        r.set_value("right_motor", 0)
        r.update_position()
        s.draw()
        w.printer(w.img())
        # print "X = " + str(r.X)
        # print "Y = " + str(r.Y)
        # print r.ltheta
        time.sleep(r.tick_rate)
