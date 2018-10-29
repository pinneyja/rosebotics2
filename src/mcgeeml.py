"""
  Capstone Project.  Code written by PUT_YOUR_NAME_HERE.
  Fall term, 2018-2019.
"""

import rosebotics as rb
import time


def main():
    """ Runs YOUR specific part of the project """
    robot = rb.Snatch3rRobot()
    color1 = rb.Color.BROWN.value
    find_color(color1, robot)


def find_color(color, robo):
    robo.drive_system.start_moving()
    while True:
        if robo.color_sensor.get_color() == color:
            robo.drive_system.stop_moving(stop_action='brake')
            break



main()
