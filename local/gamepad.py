import math
import time
import pygame

class Gamepad:
    tolerance = 0.15
    inputMode = False #True = joystick
    def __init__(self):
        pygame.display.init()
        pygame.joystick.init()
        if pygame.joystick.get_count():
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            Gamepad.inputMode = True
        else:
            self.joystick_left_x = 0
            self.joystick_left_y = 0
            self.joystick_right_x = 0
            self.joystick_right_y = 0

    def get_value(self, device):
        pygame.event.pump()
        if Gamepad.inputMode:
            if (device == "joystick_left_x"):
                value = self.joystick.get_axis(0)
            elif (device == "joystick_left_y"):
                value = self.joystick.get_axis(1)
            elif (device == "joystick_right_x"):
                value = self.joystick.get_axis(2)
            elif (device == "joystick_right_y"):
                value = self.joystick.get_axis(3)
            else:
                raise KeyError("Cannot find input: " + device)
            if abs(value) < Gamepad.tolerance:
                value = 0
        else:
            updateKeys()
            if (device == "joystick_left_x"):
                value = self.joystick_left_x
            elif (device == "joystick_left_y"):
                value = self.joystick_left_y
            elif (device == "joystick_right_x"):
                value = self.joystick_right_x
            elif (device == "joystick_right_y"):
                value = self.joystick_right_y
            else:
                raise KeyError("Cannot find input: " + device)
        return value
    def updateKeys(self):
        keys = pygame.key.get_pressed()
        print(keys)
        # if keys[pygame.K_w] and !keys[pygame.K_s]:
        #     self.joystick_left_y = -1
        # elif keys[pygame.K_s] and !keys[pygame.K_w]:
        #     self.joystick_left_y = 1
        # else:
        #     self.joystick_left_y = 0
        #
        # if keys[pygame.K_a] and !keys[pygame.K_d]:
        #     self.joystick_left_x = -1
        # elif keys[pygame.K_d] and !keys[pygame.K_a]:
        #     self.joystick_left_x = 1
        # else:
        #     self.joystick_left_x = 0
        #
        # if keys[pygame.K_i] and !keys[pygame.K_k]:
        #     self.joystick_right_y = -1
        # elif keys[pygame.K_k] and !keys[pygame.K_i]:
        #     self.joystick_right_y = 1
        # else:
        #     self.joystick_right_y = 0
        #
        # if keys[pygame.K_j] and !keys[pygame.K_l]:
        #     self.joystick_right_x = -1
        # elif keys[pygame.K_l] and !keys[pygame.K_j]:
        #     self.joystick_right_x = 1
        # else:
        #     self.joystick_right_x = 0


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
                        -self.get_value("joystick_left_y"))

    def rtheta(self):
        return Gamepad.theta(
                    self.get_value("joystick_right_x"),
                        -self.get_value("joystick_right_y"))

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

if __name__ == "__main__":
    pygame.display.init()
    pygame.joystick.init()
    print(pygame.joystick.get_count())
    controller = pygame.joystick.Joystick(0)
    controller.init()
    print(controller.get_id())
    print(controller.get_name())
    print(controller.get_numaxes())
    while True:
        pygame.event.pump()
        for i in range(controller.get_numaxes()):
            print(str(i) + " " + str(controller.get_axis(i)))
        time.sleep(0.5)
