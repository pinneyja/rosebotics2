"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

Also: responds to Beacon button-presses by beeping, speaking.

This module runs on the ROBOT.
It uses MQTT to RECEIVE information from a program running on the LAPTOP.

Authors:  David Mutchler, his colleagues, and Myon McGee.
"""
# ------------------------------------------------------------------------------
# DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# TODO: 2. With your instructor, review the "big picture" of laptop-robot
# TODO:    communication, per the comment in mqtt_sender.py.
# TODO:    Once you understand the "big picture", delete this TODO.
# ------------------------------------------------------------------------------

import rosebotics_new as rb
import time
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3


def main():
    robot = rb.Snatch3rRobot()
    remote = RemoteControlEtc(robot)
    mqtt_client = com.MqttClient(remote)
    mqtt_client.connect_to_pc()

    while True:
        time.sleep(.01)


class RemoteControlEtc(object):
    def __init__(self, robot):
        """
        stores the robot.
            :type robot: rb.Snatch3rRobot
        """
        self.robot = robot

    def forward(self, speed_string):
        speed = int(speed_string)
        inches = .5
        while True:
            if self.robot.color_sensor.get_color() == 6:
                self.robot.drive_system.stop_moving()
            elif self.robot.camera.get_biggest_blob().get_area() >= (96 * inches)**2:
                ev3.Sound.speak('something is in my way')
                self.robot.drive_system.stop_moving()
                break
            else:
                self.robot.drive_system.start_moving(speed, speed)

    def backward(self, speed_string):
        speed = -int(speed_string)
        self.robot.drive_system.start_moving(speed, speed)

    def right(self, speed_string):
        speed = int(speed_string)
        self.robot.drive_system.start_moving(-speed, speed)

    def left(self, speed_string):
        speed = int(speed_string)
        self.robot.drive_system.start_moving(speed, -speed)

    def stopper(self):
        self.robot.drive_system.stop_moving()

    def booster(self, speed_input):
        speed = int(speed_input)*2
        self.robot.drive_system.start_moving(speed, speed)

    def lift(self):
        self.robot.arm.raise_arm_and_close_claw()

    def drop(self):
        self.robot.arm.calibrate()


main()