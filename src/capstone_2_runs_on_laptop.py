"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

This module runs on your LAPTOP.
It uses MQTT to SEND information to a program running on the ROBOT.

Authors:  David Mutchler, his colleagues, and Jacob Pinney.
"""
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    """ Constructs and runs a GUI for this program. """
    sender = com.MqttClient()
    sender.connect_to_ev3()

    root = tkinter.Tk()
    setup_gui(root, sender)

    root.mainloop()
    # --------------------------------------------------------------------------
    # TODO: 5. Add code above that constructs a   com.MqttClient   that will
    # TODO:    be used to send commands to the robot.  Connect it to this pc.
    # TODO:    Test.  When OK, delete this TODO.
    # --------------------------------------------------------------------------


def setup_gui(root_window, sender_obj):
    """ Constructs and sets up widgets on the given window. """
    frame = ttk.Frame(root_window, padding=10)
    frame.grid()

    speed_entry_box = ttk.Entry(frame)
    go_forward_button = ttk.Button(frame, text="Go forward")
    stop_button = ttk.Button(frame, text="Stop")

    speed_entry_box.grid()
    go_forward_button.grid()
    stop_button.grid()

    go_forward_button['command'] = \
        lambda: handle_go_forward(speed_entry_box, sender_obj)
    stop_button['command'] = \
        lambda: handle_stop(sender_obj)


def handle_go_forward(entry_box, mqtt_obj):
    """
    Tells the robot to go forward at the speed specified in the given entry box.
    """
    speed_string = entry_box.get()
    print("go_forward, value:", speed_string)
    mqtt_obj.send_message("go_forward", [speed_string])


def handle_stop(mqtt_obj):
    mqtt_obj.send_message("stop", [])

main()
