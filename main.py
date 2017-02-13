from pimulator import Robot, Gamepad, Simulator

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
    # left_y = Gamepad.get_value("joystick_left_y")
    # turningSpeed = turningSpeed * abs(turningSpeed)
    # left_y = left_y * abs(left_y)
    # Robot.set_value("left_motor", max(min(-(left_y + turningSpeed), 1.0), -1.0))
    # Robot.set_value("right_motor", max(min(left_y - turningSpeed, 1.0), -1.0))


# Do not delete the line below: it runs the simulator!
Simulator.simulate()
