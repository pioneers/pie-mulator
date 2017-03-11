from pimulator import Robot, Gamepad, Simulator


def teleop_setup():
    Robot.set_value("left_motor", "duty_cycle", 1)
    Robot.set_value("right_motor", "duty_cycle", -1)

def teleop_main():
    pass












# Do not delete the line below: it runs the simulator!
Simulator.simulate(teleop_setup, teleop_main)
