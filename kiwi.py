import math
import time

class Robot:
    tick_rate = 0.1            #in s
    width = 12                   #width of robot
    w_radius = 2               #radius of a wheel
    MAX_X = 143
    MAX_Y = 143
    neg = -1                    #negate left motor calculation
    def __init__ (self):
        self.X = 72.0           #X position of the robot
        self.Y = 72.0           #Y position of the robot
        self.Wl = 0.0           #angular velocity of l wheel, degree/s
        self.Wr = 0.0           #angular velocity of r wheel, degree/s
        self.ltheta = 0.0       #angular position of l wheel, in degree
        self.rtheta = 0.0       #angular position of r wheel, in degree
        self.dir = 90.0           #Direction of the robot facing,in degree

    """ DifferentialDrive Calculation Credits to:
    https://chess.eecs.berkeley.edu/eecs149/documentation/differentialDrive.pdf
    """
    def update_position(self):
        lv = self.Wl * Robot.w_radius * Robot.neg
        rv = self.Wr * Robot.w_radius
        radian = math.radians(self.dir)
        if (lv == rv):
            distance = rv * Robot.tick_rate
            dx = distance *math.cos(radian)
            dy = distance *math.sin(radian)
            print(dx)
            print(dy)
        else:
            rt = Robot.width/2 * (lv+rv)/(rv-lv)
            Wt = (rv-lv)/Robot.width
            theta = Wt* Robot.tick_rate
            i = rt * (1 - math.cos(theta))
            j = math.sin(theta)* rt
            dx = i*math.sin(radian) + j*math.cos(radian)
            dy = i*math.cos(radian) + j*math.sin(radian)
            self.dir = (self.dir + math.degrees(theta))%360

        self.X = max(min(self.X + dx, Robot.MAX_X),0)
        self.Y = max(min(self.Y + dy, Robot.MAX_Y),0)
        self.ltheta = (self.Wl * 5+ self.ltheta) % 360
        self.rtheta = (self.Wr * 5+ self.rtheta) % 360

    def set_value(self, device, speed):
        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed cannot be great than 1.0 or less than -1.0.")
        if (device == "left_motor"):
            self.Wl = speed * 9
        elif device == "right_motor":
            self.Wr = speed * 9
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
    SCREEN_HEIGHT = 48.0
    SCREEN_WIDTH = 48.0

    def __init__(self, robot):
        self.robot = robot

    def draw(self):
        k = Screen.SCREEN_HEIGHT/144.0 #screen scaling coefficient
        # print (self.robot.X*k)
        for y in range(int(Screen.SCREEN_HEIGHT)):
            line = ["."] * int(Screen.SCREEN_WIDTH)
            for x in range(int(Screen.SCREEN_WIDTH)):
                if ((self.robot.X*k)//1 == x and (self.robot.Y*k)// 1 == y):
                    line[x] = "@"
            print(' '.join(line))
        print("__"* int(Screen.SCREEN_WIDTH))

if __name__ == "__main__":
    r = Robot()
    w = Wheel(r)
    s = Screen(r)
    while True:
        r.set_value("left_motor", -1)
        r.set_value("right_motor", 1)
        r.update_position()
        s.draw()
        w.printer(w.img())
        print "X = " + str(r.X)
        print "Y = " + str(r.Y)
        # print r.ltheta
        time.sleep(r.tick_rate)
