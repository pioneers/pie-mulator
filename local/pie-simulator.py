import time
from robot import *
from gamepad import *
from screen import *


def setup():
    pass

def loop():
    """Driving straight. """
    # Robot.set_value("left_motor", 0.7)
    # Robot.set_value("right_motor", -0.7)
    """Tank Drive"""
    Robot.set_value("left_motor", -Gamepad.get_value("joystick_left_y"))
    Robot.set_value("right_motor", Gamepad.get_value("joystick_right_y"))
    """Arcade Drive"""
    # turningSpeed =  Gamepad.get_value("joystick_left_x")
    # Robot.set_value("left_motor", -(Gamepad.get_value("joystick_left_y") + turningSpeed))
    # Robot.set_value("right_motor", Gamepad.get_value("joystick_left_y") - turningSpeed)

if __name__ == "__main__":
    # Execute user-defined actions
    setup()
    Robot = Robot()
    Gamepad = Gamepad()
    Screen = Screen(Robot, Gamepad, 48)

    while True:
        # Execute user-defined actions
        loop()
        # Update the robot and print the new state to the screen
        Robot.update_position()
        Screen.draw()
        # Wait the appropriate amount of time
        time.sleep(Robot.tick_rate)