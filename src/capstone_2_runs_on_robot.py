"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

Also: responds to Beacon button-presses by beeping, speaking.

This module runs on the ROBOT.
It uses MQTT to RECEIVE information from a program running on the LAPTOP.

Authors:  David Mutchler, his colleagues, and Jacob Pinney.
"""

import rosebotics_new as rb
import mqtt_remote_method_calls as com
import time
# import ev3dev.ev3 as ev3


def main():
    robot = rb.Snatch3rRobot()

    mqtt_client_sender = com.MqttClient()
    mqtt_client_sender.connect_to_pc()
    sender = Sender(mqtt_client_sender)

    receiver = Receiver(robot, sender)
    mqtt_client = com.MqttClient(receiver)
    mqtt_client.connect_to_pc()

    while True:
        # print(robot.proximity_sensor.get_distance_to_nearest_object_in_inches())
        time.sleep(0.01)

    # beacon = rb.InfraredAsBeaconButtonSensor()
    # while True:
    #     if beacon.is_top_red_button_pressed():
    #         ev3.Sound.beep().wait()
    #     if beacon.is_top_blue_button_pressed():
    #         ev3.Sound.speak("Hello. How are you?")
    #     time.sleep(0.01)  # For the delegate to do its work


class Sender(object):
    def __init__(self, mqtt_client):
        """
        :type  mqtt_client:  com.MqttClient
        """
        self.mqtt_client = mqtt_client

    def send_sonar_data(self, seq_of_seq):
        self.mqtt_client.send_message("sonar", [seq_of_seq])


class Receiver(object):
    def __init__(self, robot, sender):
        """
        :type robot: rb.Snatch3rRobot
        """
        self.robot = robot
        self.sender = sender

    # def go_forward(self, speed_string):
    #     # makes the robot go forward at the given speed
    #     speed = int(speed_string)
    #     self.robot.drive_system.start_moving(speed, speed)
    #
    # def stop(self):
    #     self.robot.drive_system.stop_moving()

    def go(self, left_stop_action, right_stop_action):
        self.robot.drive_system.start_moving(left_stop_action, right_stop_action)

    def sonar(self, degrees_to_spin):
        data_one = self.robot.drive_system.spin_in_place_degrees(degrees_to_spin, duty_cycle_percent=100, collect_sonar=True, robot=self.robot)
        # data_two = self.robot.drive_system.spin_in_place_degrees(360, duty_cycle_percent=100, collect_sonar=True, robot=self.robot)
        # data_three = self.robot.drive_system.spin_in_place_degrees(365, duty_cycle_percent=100, collect_sonar=True, robot=self.robot)
        # data_four = self.robot.drive_system.spin_in_place_degrees(360, duty_cycle_percent=100, collect_sonar=True, robot=self.robot)
        # data_five = self.robot.drive_system.spin_in_place_degrees(360, duty_cycle_percent=100, collect_sonar=True, robot=self.robot)
        seq_of_seq_of_seq = [data_one]#, data_two, data_three]#, data_four, data_five]
        big_dic = {}
        for seq in seq_of_seq_of_seq:
            for seq_of_two in seq:
                if seq_of_two[0] in big_dic:
                    big_dic[seq_of_two[0]] = (seq_of_two[1] + big_dic[seq_of_two[0]]) / 2
                else:
                    big_dic[seq_of_two[0]] = seq_of_two[1]
        self.sender.send_sonar_data(data_one)#big_dic)


main()
