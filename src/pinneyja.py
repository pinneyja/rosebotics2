"""
  Capstone Project.  Code written by PUT_YOUR_NAME_HERE.
  Fall term, 2018-2019.
"""

import rosebotics as rb
import time


def main():
    """ Runs YOUR specific part of the project """
    robot = rb.Snatch3rRobot()
    follow_black_line(robot, False)


def follow_black_line(robot, isCounterclockwise):
    # isCounterclockwise == True then robot is turning left
    # else                                  is turning right
    # assumes robot is placed on black line to start

    if isCounterclockwise:
        value = -1
    else:
        value = 1

    color = rb.Color.BLACK.value
    while True:
        robot.drive_system.start_moving(30, 30)
        if robot.color_sensor.get_color() != color:
            robot.drive_system.stop_moving("brake")
            while True:
                robot.drive_system.spin_in_place_degrees(value)
                if robot.color_sensor.get_color() == color:
                    break


main()
