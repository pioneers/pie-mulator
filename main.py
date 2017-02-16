from pimulator import Robot, Gamepad, Actions, Simulator

async def drive_fwd():
    Robot.set_value("left_motor", 0.7)
    Robot.set_value("right_motor", -0.7)
    await Actions.sleep(1.0)
    Robot.set_value("left_motor", 0.)
    Robot.set_value("right_motor", -0.)
    await Actions.sleep(1.0)

def setup():
    Robot.run(drive_fwd)

def loop():
    if Robot.is_running(drive_fwd):
        return # wait until it completes

    driving_mode = 0

    if driving_mode == 0:
        """Driving straight. """
        # Robot.set_value("left_motor", 0.7)
        # Robot.set_value("right_motor", -0.7)
    elif driving_mode == 1:
        """Tank Drive"""
        # Robot.set_value("left_motor", Gamepad.get_value("joystick_left_y"))
        # Robot.set_value("right_motor", -Gamepad.get_value("joystick_right_y"))
    elif driving_mode == 2:
        """Arcade Drive"""
        turningSpeed =  Gamepad.get_value("joystick_left_x")
        left_y = -Gamepad.get_value("joystick_left_y")
        turningSpeed = turningSpeed * abs(turningSpeed)
        left_y = left_y * abs(left_y)
        Robot.set_value("left_motor", max(min(-(left_y + turningSpeed), 1.0), -1.0))
        Robot.set_value("right_motor", max(min(left_y - turningSpeed, 1.0), -1.0))


# Do not delete the line below: it runs the simulator!
Simulator.simulate()
