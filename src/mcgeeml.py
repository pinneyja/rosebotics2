"""
  Capstone Project.  Code written by PUT_YOUR_NAME_HERE.
  Fall term, 2018-2019.
"""

import rosebotics_new as rb
import ev3dev.ev3 as ev3
import time


def main():
    """ Runs YOUR specific part of the project """
    robot = rb.Snatch3rRobot()
    #color1 = rb.Color.BROWN.value
    #find_color(color1, robot)
    object_area(robot)


def find_color(color, robo):
    robo.drive_system.start_moving()
    while True:
        if robo.color_sensor.get_color() == color:
            robo.drive_system.stop_moving(stop_action='brake')
            break


def object_area(robo):
    while True:
        print(robo.camera.get_biggest_blob().get_area())
        if robo.camera.get_biggest_blob().get_area() >= 12:
            ev3.Sound.beep().wait()

main()
