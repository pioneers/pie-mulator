import math
import time

class Gamepad:
              #0, #1, #2, #3
    sets = [[[ 0,  0,  0,  0],     #joystick_left_x
             [ 1,  1, -1, -1],     #joystick_left_y
             [ 0,  0,  0,  0],     #joystick_right_x
             [ 1, -1, -1,  1],     #joystick_right_y
             [ 1,  2,  3,  3]],    #Duration s

            [[ 0,  1,  0, -1],
             [ 1,  0, -1,  0],
             [ 0,  0,  0,  0],
             [ 0,  0,  0,  0],
             [ 3,  3,  3,  3]]
            ]


    def __init__(self, set_num):
        self.set_num = set_num
        self.t0 = time.time()
        self.joystick_left_x = Gamepad.sets[set_num][0]
        self.joystick_left_y =  Gamepad.sets[set_num][1]
        self.joystick_right_x =  Gamepad.sets[set_num][2]
        self.joystick_right_y =  Gamepad.sets[set_num][3]
        self.durations = Gamepad.sets[set_num][4]         #lst of instr duration
        self.i = 0                                        #index of insturction

    def get_value(self, device):
        now = time.time()
        timePassed = now - self.t0
        if  (timePassed >= self.durations[self.i]):
            self.i = (self.i + 1) % len(self.durations)
            self.t0 = now
        print(timePassed)

        if (device == "joystick_left_x"):
            return self.joystick_left_x[self.i]
        if (device == "joystick_left_y"):
            return self.joystick_left_y[self.i]
        if (device == "joystick_right_x"):
            return self.joystick_right_x[self.i]
        if (device == "joystick_right_y"):
            return self.joystick_right_y[self.i]
        else:
            raise KeyError("Cannot find input: " + device)

    def godmode(self, device, value):
        if value > 1.0 or value < -1.0:
            raise ValueError("Value cannot be great than 1.0 or less than -1.0.")
        if (device == "joystick_left_x"):
            self.joystick_left_x = value
        elif (device == "joystick_left_y"):
            self.joystick_left_y = value
        elif (device == "joystick_right_x"):
            self.joystick_right_x = value
        elif (device == "joystick_right_y"):
            self.joystick_right_y = value
        else:
            raise KeyError("Cannot find input: " + device)

    def ltheta(self):
        return Gamepad.theta(
                    self.get_value("joystick_left_x"),
                        self.get_value("joystick_left_y"))

    def rtheta(self):
        return Gamepad.theta(
                    self.get_value("joystick_right_x"),
                        self.get_value("joystick_right_y"))

    def theta(x, y):
        """Convert cartesian to polar coordinates and return the radius."""
        if (x == 0 and y == 0):
            return "Neutral"
        if x == 0:
            if y > 0:
                return 90.0
            else:
                return 270.0
        theta = math.degrees(math.atan(y / x))
        if x > 0:
            return theta
        else:
            return theta + 180.0
