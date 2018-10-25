"""
  Capstone Project.  Code written by PUT_YOUR_NAME_HERE.
  Fall term, 2018-2019.
"""

import rosebotics as rb
import time


def main():
    """ Runs YOUR specific part of the project """
    q = True
    robot = rb.Snatch3rRobot()
    robot.drive_system.left_wheel.reset_degrees_spun()
    robot.drive_system.left_wheel.start_spinning(100)
    robot.drive_system.right_wheel.start_spinning(100)
    while q is True:
        if robot.drive_system.left_wheel.get_degrees_spun() >= 100:
            q = False
    robot.drive_system.left_wheel.stop_spinning()
    robot.drive_system.right_wheel.stop_spinning()


main()
