class Gamepad
    joystick_left_x = 0
    joystick_left_y = 0
    joystick_right_x = 0
    joystick_right_y = 0
    
    def __init__(self):

    def get_value(self, device):
        if (device = "joystick_left_x"):
            return Gamepad.joystick_left_x
        if (device = "joystick_left_y"):
            return Gamepad.joystick_left_y
        if (device = "joystick_right_x"):
            return Gamepad.joystick_right_x
        if (device = "joystick_right_y"):
            return Gamepad.joystick_right_y
        else:
            raise KeyError("Cannot find input: " + deivce)


    def godmode(self, input, value):
        if (device = "joystick_left_x"):
            Gamepad.joystick_left_x = value
        if (device = "joystick_left_y"):
            Gamepad.joystick_left_y = value
        if (device = "joystick_right_x"):
            Gamepad.joystick_right_x = value
        if (device = "joystick_right_y"):
            Gamepad.joystick_right_y = value
        else:
            raise KeyError("Cannot find input: " + deivce)
