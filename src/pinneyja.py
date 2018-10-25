"""
  Capstone Project.  Code written by PUT_YOUR_NAME_HERE.
  Fall term, 2018-2019.
"""

import rosebotics as rb
import time


def main():
    """ Runs YOUR specific part of the project """
    robot = rb.Snatch3rRobot()
    robot.drive_system.left_wheel.reset_degrees_spun()
    robot.drive_system.left_wheel.start_spinning(100)
    while True:
        if robot.drive_system.left_wheel.get_degrees_spun() > 1150:
            robot.drive_system.left_wheel.stop_spinning()
            break

main()
