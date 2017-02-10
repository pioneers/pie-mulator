class Gamepad:

    def __init__(self):
        self.joystick_left_x = 0
        self.joystick_left_y = 0
        self.joystick_right_x = 0
        self.joystick_right_y = 0

    def get_value(self, device):
        if (device == "joystick_left_x"):
            return self.joystick_left_x
        if (device == "joystick_left_y"):
            return self.joystick_left_y
        if (device == "joystick_right_x"):
            return self.joystick_right_x
        if (device == "joystick_right_y"):
            return self.joystick_right_y
        else:
            raise KeyError("Cannot find input: " + deivce)


    def godmode(self, input, value):
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
            raise KeyError("Cannot find input: " + deivce)

    def ltheta(self):
        return self.theta(self.joystick_left_x, self.joystick_left_y)

    def rtheta(self):
        return self.theta(self.joystick_right_x, self.joystick_right_y)

    def theta(x, y):
        if (x == 0 and y == 0):
            return "Neutral"
        theta = math.degrees(math.atan(y / x))
        if x == 0:
            if y > 0:
                return 90.0
            else:
                return 270.0
        elif x > 0:
            return theta
        else:
            return theta + 180.0
