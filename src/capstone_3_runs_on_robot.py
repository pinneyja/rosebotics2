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
    # --------------------------------------------------------------------------
    # TODO: 3. Construct a Snatch3rRobot.  Test.  When OK, delete this TODO.
    # --------------------------------------------------------------------------

    robo = rb.Snatch3rRobot()


    # --------------------------------------------------------------------------
    # TODO: 4. Add code that constructs a   com.MqttClient   that will
    # TODO:    be used to receive commands sent by the laptop.
    # TODO:    Connect it to this robot.  Test.  When OK, delete this TODO.
    # --------------------------------------------------------------------------
    rc = RemoteControlEtc(robo)
    mqtt_client = com.MqttClient(rc)
    mqtt_client.connect_to_pc()

    # --------------------------------------------------------------------------
    # TODO: 5. Add a class for your "delegate" object that will handle messages
    # TODO:    sent from the laptop.  Construct an instance of the class and
    # TODO:    pass it to the MqttClient constructor above.  Augment the class
    # TODO:    as needed for that, and also to handle the go_forward message.
    # TODO:    Test by PRINTING, then with robot.  When OK, delete this TODO.
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # TODO: 6. With your instructor, discuss why the following WHILE loop,
    # TODO:    that appears to do nothing, is necessary.
    # TODO:    When you understand this, delete this TODO.
    # --------------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # TODO: 7. Add code that makes the robot beep if the top-red button
    # TODO:    on the Beacon is pressed.  Add code that makes the robot
    # TODO:    speak "Hello. How are you?" if the top-blue button on the
    # TODO:    Beacon is pressed.  Test.  When done, delete this TODO.
    # ----------------------------------------------------------------------


class RemoteControlEtc(object):
    def __init__(self, robot):
        """
        stores the robot.
            :type robot: rb.Snatch3rRobot
        """
        self.robot = robot
        self.speed = None
        self.initialized = False

    def movement(self, speed_string):
        #stores the robot's given speed
        print("telling the robot to start moving at: ", speed_string)
        speed = int(speed_string)
        if self.initialized == False:
            self.speed = speed
            self.initialized = True

        while True:

            self.object_area(2)

            if self.robot.beacon_button_sensor.is_top_blue_button_pressed():
                self.robot.drive_system.start_moving(self.speed/2, self.speed)

            if self.robot.beacon_button_sensor.is_top_red_button_pressed():
                self.robot.drive_system.start_moving(self.speed, self.speed/2)

            if self.robot.beacon_button_sensor.is_bottom_blue_button_pressed():
                self.robot.drive_system.start_moving(-self.speed, -self.speed/2)

            if self.robot.beacon_button_sensor.is_bottom_red_button_pressed():
                self.robot.drive_system.start_moving(-self.speed/2, -self.speed)

            if self.robot.beacon_button_sensor.is_top_red_button_pressed() and self.robot.beacon_button_sensor.is_top_blue_button_pressed():
                self.robot.drive_system.start_moving(self.speed, self.speed)

            if self.robot.beacon_button_sensor.is_bottom_red_button_pressed() and self.robot.beacon_button_sensor.is_bottom_blue_button_pressed():
                self.robot.drive_system.start_moving(self.speed, self.speed)



    def object_area(self, num):
        if self.robot.camera.get_biggest_blob().get_area() >= (96 * num) ** 2:
            self.robot.drive_system.start_moving(-self.speed, -self.speed)
            ev3.Sound.speak('Something is in my way.')


main()