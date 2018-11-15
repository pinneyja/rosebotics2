"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

This module runs on your LAPTOP.
It uses MQTT to SEND information to a program running on the ROBOT.

Authors:  David Mutchler, his colleagues, and Myon McGee.
"""
# ------------------------------------------------------------------------------
# done: 1. PUT YOUR NAME IN THE ABOVE LINE.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    """ Constructs and runs a GUI for this program. """
    root = tkinter.Tk()
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    setup_gui(root, mqtt_client)

    root.mainloop()

def setup_gui(root_window, user):

    """ Constructs and sets up widgets on the given window. """
    frame = ttk.Frame(root_window, padding=100)
    frame.grid()

    speed_entry_box = ttk.Entry(frame)
    backward_entry_box = ttk.Entry(frame)
    left_entry_box = ttk.Entry(frame)
    right_entry_box = ttk.Entry(frame)
    speed_button = ttk.Button(frame, text="Forward")
    backward_botton = ttk.Button(frame, text="Backward")
    left_botton = ttk.Button(frame, text="Left")
    right_botton = ttk.Button(frame, text="Right")
    label = ttk.Label(frame, text="The Racer")
    entry_box = ttk.Entry(frame)

    label.grid()
    backward_entry_box.grid()
    backward_botton.grid()
    left_entry_box.grid()
    left_botton.grid()
    right_entry_box.grid()
    right_botton.grid()
    speed_entry_box.grid()
    speed_button.grid()
    entry_box.grid()

    speed_button['command'] = \
        lambda: handle_go_forward(user, speed_entry_box)
    backward_botton['command'] = \
        lambda: backwards(user, backward_entry_box)
    left_botton['command'] = \
        lambda: lefts(user, left_entry_box)
    right_botton['command'] = \
        lambda: rights(user, right_entry_box)

    root_window.bind_all('<Key-w>', lambda event: handle_go_forward(user, speed_entry_box))
    root_window.bind_all('<Key-s>', lambda event: backwards(user, backward_entry_box))
    root_window.bind_all('<Key-d>', lambda event: lefts(user, left_entry_box))
    root_window.bind_all('<Key-a>', lambda event: rights(user, right_entry_box))
    root_window.bind_all('<Key-b>', lambda event: boost(user, speed_entry_box))
    root_window.bind_all('<Key-space>', lambda event: stop(user))
    root_window.bind_all('<Key-p>', lambda event: lifts(user))
    root_window.bind_all('<Key-o>', lambda event: drops(user))

    root_window.mainloop()

def stop(mqtt_client):

    mqtt_client.send_message('stopper')

def lifts(mqtt_client):

    mqtt_client.send_message('lift')

def drops(mqtt_client):

    mqtt_client.send_message('drop')


def boost(mqtt_client, speed_input):

    speed_string = speed_input.get()
    mqtt_client.send_message('booster', [speed_string])


def handle_go_forward(mqtt_client, speed_input):

    speed_string = speed_input.get()
    mqtt_client.send_message('forward', [speed_string])


def backwards(mqtt_client, speed_input):

    speed_string = speed_input.get()
    mqtt_client.send_message('backward', [speed_string])


def lefts(mqtt_client, speed_input):
    speed_string = speed_input.get()
    mqtt_client.send_message('left', [speed_string])


def rights(mqtt_client, speed_input):
    speed_string = speed_input.get()
    mqtt_client.send_message('right', [speed_string])


main()
