"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

Also: responds to Beacon button-presses by beeping, speaking.

This module runs on the ROBOT.
It uses MQTT to RECEIVE information from a program running on the LAPTOP.

Authors:  David Mutchler, his colleagues, and Hunter Hicks.
"""
import rosebotics_new as rb
import time
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import math


def main():
    bot = rb.Snatch3rRobot()

    rc = RemoteControlEtc(bot)

    client = com.MqttClient(rc)
    client.connect_to_pc()
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
    while True:
        # ----------------------------------------------------------------------
        # TODO: 7. Add code that makes the robot beep if the top-red button
        # TODO:    on the Beacon is pressed.  Add code that makes the robot
        # TODO:    speak "Hello. How are you?" if the top-blue button on the
        # TODO:    Beacon is pressed.  Test.  When done, delete this TODO.
        # ----------------------------------------------------------------------
        if bot.beacon_button_sensor.is_top_red_button_pressed():
            ev3.Sound.beep().wait()
            time.sleep(0.01)
        if bot.beacon_button_sensor.is_top_blue_button_pressed():
            ev3.Sound.speak('Hello. How are you?').wait()
            time.sleep(0.01)


class RemoteControlEtc(object):
    def __init__(self, bot):
        self.bot = bot
        self.direction = 0
        self.multiplier = 1
        self.speed = 100
        self.toggle = 0

    def speed_setup(self, speed_string):
        try:
            speed = int(speed_string)
        except:
            speed = 100

        self.speed = speed

    def multiplier_setup(self, multiplier_string):
        try:
            multiplier = int(multiplier_string)
        except:
            multiplier = 1

        self.multiplier = multiplier

    def change_value(self, value):
        try:
            value = int(value)
        except:
            value = 0

        self.toggle = value
        print(self.toggle)

    def coordinate_setup(self, coordinate_list):
        print("***")
        print(coordinate_list)
        print("***")

        list = []
        for k in range(0, len(coordinate_list) - 1, 2):
            pointlist = []
            pointlist = pointlist + [coordinate_list[k]]
            pointlist = pointlist + [coordinate_list[k + 1]]
            list = list + [pointlist]

        print("***Finished List***")
        print(list)
        print("***Finished List***")

        self.drive_start(list)

    def drive_start(self, list):
        if len(list) < 2:
            print(list)
            print("ERROR")
            return

        for k in range(len(list) - 1):
            xpos = list[k][0]
            ypos = list[k][1]
            xfpos = list[k + 1][0]
            yfpos = list[k + 1][1]
            x = xfpos - xpos
            y = yfpos - ypos
            if (x == 0) or (y == 0):
                if (x == 0):
                    self.bot.drive_system.go_straight_inches(((y / 111) * self.multiplier), self.speed)
                else:
                    if (x < 0):
                        self.bot.drive_system.spin_in_place_degrees(-90)
                        self.bot.drive_system.go_straight_inches(((x / 111) * self.multiplier), self.speed)
                        self.bot.drive_system.spin_in_place_degrees(90)
                    else:
                        self.bot.drive_system.spin_in_place_degrees(90)
                        self.bot.drive_system.go_straight_inches(((x / 111) * self.multiplier), self.speed)
                        self.bot.drive_system.spin_in_place_degrees(-90)
            else:
                print("X move and Y move")
                print("X:", x)
                print("Y:", y)
                print("*****************")
                distance = math.sqrt(((x ** 2) + (y ** 2)))
                distance = ((distance / 111) * self.multiplier)
                print("***Distance Traveling (in inches)***")
                print(distance)
                print("************************************")
                if yfpos < ypos:
                    theta = math.atan(((abs(y)) / (abs(x))))
                    theta = ((theta * 180) / math.pi)
                    theta = 90 - theta
                else:
                    theta = math.atan(((abs(x)) / (abs(y))))
                    theta = ((theta * 180) / math.pi)
                    theta = 180 - theta
                print("***Turning Angle (in degrees)***")
                print(theta)
                print("********************************")
                dis = distance / 80
                i = 0
                if (x < 0):
                    self.bot.drive_system.spin_in_place_degrees(-theta)
                    if self.toggle == 1:
                        while True:
                            if i < distance:
                                self.bot.drive_system.go_straight_inches(dis, self.speed)
                                i = i + dis
                            else:
                                break

                            if (70 * ((self.bot.proximity_sensor.get_distance_to_nearest_object()) / 100)) < 10:
                                self.bot.drive_system.stop_moving()
                                ev3.Sound.speak('There is an object in my path!')
                                return
                    else:
                        self.bot.drive_system.go_straight_inches(distance, self.speed)
                    self.bot.drive_system.spin_in_place_degrees(theta)
                else:
                    self.bot.drive_system.spin_in_place_degrees(theta)
                    if self.toggle == 1:
                        while True:
                            if i < distance:
                                self.bot.drive_system.go_straight_inches(dis, self.speed)
                                i = i + dis
                            else:
                                break

                            if (70 * ((self.bot.proximity_sensor.get_distance_to_nearest_object()) / 100)) < 10:
                                self.bot.drive_system.stop_moving()
                                ev3.Sound.speak('There is an object in my path!')
                                return
                    else:
                        self.bot.drive_system.go_straight_inches(distance, self.speed)
                    self.bot.drive_system.spin_in_place_degrees(-theta)

    def go_forward(self, speed_string):
        try:
            speed = int(speed_string)
        except:
            speed = 100
        self.bot.drive_system.start_moving(speed, speed)

    def go_backward(self, speed_string):
        try:
            speed = int(speed_string)
            speed = -speed
        except:
            speed = -100

        self.bot.drive_system.start_moving(speed, speed)

    def spin_left(self, degree_string):
        try:
            degrees = int(degree_string)
            degrees = -degrees
        except:
            degrees = -90

        self.bot.drive_system.spin_in_place_degrees(degrees)

    def spin_right(self, degree_string):
        try:
            degrees = int(degree_string)
            degrees = degrees
        except:
            degrees = -90

        self.bot.drive_system.spinss_in_place_degrees(degrees)

    def stop(self):
        self.bot.drive_system.stop_moving()

    def move_inches(self, inches_string):
        try:
            inches = int(inches_string)
        except:
            inches = 10

        self.bot.drive_system.go_straight_inches(inches)


main()
