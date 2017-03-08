"""A simulation to demonstrate the usage of sensors without physical dependencies."""

import time
import math


def time_mod(num_states, state_length=1):
    """Given a number of state with duration state_length, returns a different state depending on the time.

    All states are equally likely.
    """
    seconds = int(time.time() / state_length)
    return seconds % num_states


class Tag(object):
    """Represents an object with a RFID tag"""
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        rep = [
            "\u250f\u2501\u2501\u2513\n",
            "\u2503 %s\u2503\n",
            "\u2517\u2501\u2501\u251B"
        ]

        return ''.join(rep) % self.name

    def __repr__(self):
        return "Tag(%s, %s)" % (self.name, self.number)


class Robot(object):
    """An access point for different sensors"""
    tags = (Tag('A', 136), Tag('B', 175), Tag('C', 73), Tag('D', 204))
    follower_states = (
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 1),
        (1, 0, 0),
        (1, 0, 1),
        (1, 1, 0),
        (1, 1, 1))

    open_switch = [
        "  *\n",
        " / \n",
        "/__\n",
        "| |\n",
        "|_|"
    ]
    closed_switch = [
        "__*\n",
        "| |\n",
        "|_|"
    ]

    wheel_base = list("* - - - *|       ||   x   ||       |* - - - *")
    width = 9

    def str_format(list_img):
        """Return a list of 5 strings each of length 9

        Args:
            list_img: A list of 5 * 9 characters
        """
        result = []
        for y in range(5):
            segment = list_img[y * Robot.width:(y + 1) * Robot.width]
            result.append(''.join(segment))
        return result

    def wheel(theta, label='*'):
        """Generate a string picturing a wheel at position theta

        Args:
            theta (float): the angular displacement of the wheel
        """

        result = Robot.wheel_base.copy()
        result[2 * Robot.width + 4] = label
        state = round(theta / 45.0) % 8

        if state == 0:
            result[1 * Robot.width + 4] = "|"
        elif state == 2:
            result[1 * Robot.width + 7] = "/"
        elif state == 2:
            result[2 * Robot.width + 7] = "-"
        elif state == 3:
            result[3 * Robot.width + 7] = "\\"
        elif state == 4:
            result[3 * Robot.width + 4] = "|"
        elif state == 5:
            result[3 * Robot.width + 1] = "/"
        elif state == 6:
            result[2 * Robot.width + 1] = "-"
        elif state == 7:
            result[1 * Robot.width + 1] = "\\"

        return Robot.str_format(result)

    def limit_switch():
        """Return the current state of the limit switch."""
        state = bool(time_mod(2))
        if state:
            print(''.join(Robot.open_switch))
        else:
            print(''.join(Robot.closed_switch))

        return state

    def potentiometer():
        """Return the current angle of the potentiometer as a float.

        The potentiometer moves from 0 to MAX_ANGLE then
        moves back from MAX_ANGLE to 0.

        The potentiometer has a period of 2 pi or roughly 6 seconds.
        """
        max_angle = 1

        angle = round((math.sin(time.time() / 2) * max_angle/2 + max_angle/2) * 100) / 100
        image = Robot.wheel(angle * 360 * .75)
        for line in image:
            print(line)

        return angle

    def rfid():
        """Return the current reading from the rfid sensor.

        The tag in front of the rfid sensor will change every second
        """

        tag = Robot.tags[time_mod(len(Robot.tags))]
        print(tag)
        return tag.number

    def line_follower(sensor_num):
        """Returns the current reading from the specified sensor"""
        assert sensor_num < 3 and sensor_num >= 0
        return Robot.follower_states[time_mod(len(Robot.follower_states))][sensor_num]


