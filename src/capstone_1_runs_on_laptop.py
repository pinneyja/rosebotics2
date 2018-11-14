"""
Mini-application:  Buttons on a Tkinter GUI tell the robot to:
  - Go forward at the speed given in an entry box.

This module runs on your LAPTOP.
It uses MQTT to SEND information to a program running on the ROBOT.

Authors:  David Mutchler, his colleagues, and Hunter Hicks.
"""

# ------------------------------------------------------------------------------
# TODO: 2. With your instructor, discuss the "big picture" of laptop-robot
# TODO:    communication:
# TODO:      - One program runs on your LAPTOP.  It displays a GUI.  When the
# TODO:        user presses a button intended to make something happen on the
# TODO:        ROBOT, the LAPTOP program sends a message to its MQTT client
# TODO:        indicating what it wants the ROBOT to do, and the MQTT client
# TODO:        SENDS that message TO a program running on the ROBOT.
# TODO:
# TODO:      - Another program runs on the ROBOT. It stays in a loop, responding
# TODO:        to events on the ROBOT (like pressing buttons on the IR Beacon).
# TODO:        It also, in the background, listens for messages TO the ROBOT
# TODO:        FROM the program running on the LAPTOP.  When it hears such a
# TODO:        message, it calls the method in the DELAGATE object's class
# TODO:        that the message indicates, sending arguments per the message.
# TODO:
# TODO:  Once you understand the "big picture", delete this TODO (if you wish).
# ------------------------------------------------------------------------------

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class PenData(object):
    def __init__(self):
        self.mouse_x = None
        self.mouse_y = None
        self.fclick = False
        self.list = []
        self.currentsetting = 'gui'


def main():
    """ Constructs and runs a GUI for this program. """
    root = tkinter.Tk()
    pendata = PenData()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    setup_gui(root, pendata, mqtt_client)

    root.mainloop()


def setup_gui(root, pendata, mqtt_client):
    frame = ttk.Frame(root)
    frame.grid()
    label1 = ttk.Label(frame, text="Draw points and click go!")
    label1.grid(pady=5)
    canvas = tkinter.Canvas(frame, width=500, height=500, background='darkgrey')
    canvas.grid(pady=5)
    button = ttk.Button(frame, text="Go!")
    button.grid(pady=5)
    label2 = ttk.Label(frame, text="Below is multiplier for inches traveling.")
    label2.grid()
    multiplier_box = ttk.Entry(frame, justify=tkinter.CENTER)
    multiplier_box.grid()
    label3 = ttk.Label(frame, text="Below is speed for driving.")
    label3.grid()
    speed_box = ttk.Entry(frame, justify=tkinter.CENTER)
    speed_box.grid()
    checkbox = ttk.Checkbutton(frame, text="Toggle Stopping Sensor")
    checkbutton_observer = tkinter.StringVar()
    checkbox['variable'] = checkbutton_observer
    checkbox.grid()
    resetbutton = ttk.Button(frame, text="Reset Drawing")
    resetbutton.grid(pady=10)
    controller_button = ttk.Button(frame, text="Switch Controls")
    controller_button.grid(pady=5)
    label4 = ttk.Label(frame, text="Below is spinning angle for controller")
    label4.grid_forget()
    spin_box = ttk.Entry(frame)
    spin_box.grid_forget()
    fix_button = ttk.Button(frame, text="Driving Button")
    fix_button.grid_forget()

    canvas.bind('<Button-1>', lambda event: mouseclick(event, canvas, pendata))
    button['command'] = (lambda: send_information(pendata, multiplier_box, speed_box, mqtt_client))
    resetbutton['command'] = (lambda: reset_coordinates(canvas, pendata))
    controller_button['command'] = lambda: (
        switch_controls(canvas, label1, label2, label3, label4, multiplier_box, spin_box, speed_box, button, fix_button,
                        resetbutton, controller_button, checkbox, pendata))
    fix_button['command'] = lambda: (stop(mqtt_client, pendata))
    checkbox['command'] = lambda: change_value(checkbutton_observer, mqtt_client)

    root.bind_all('<Key-w>', lambda event: handle_go_forward(speed_box, mqtt_client, pendata))
    root.bind_all('<Key-s>', lambda event: handle_go_backward(speed_box, mqtt_client, pendata))
    root.bind_all('<Key-a>', lambda event: handle_spin_left(spin_box, mqtt_client, pendata))
    root.bind_all('<Key-d>', lambda event: handle_spin_right(spin_box, mqtt_client, pendata))
    root.bind_all('<Key-space>', lambda event: stop(mqtt_client, pendata))


def mouseclick(event, canvas, pendata):
    canvas.create_oval(event.x - 3, event.y - 3,
                       event.x + 3, event.y + 3,
                       fill='black', width=0.5)
    if pendata.fclick == False:
        pendata.x = event.x
        pendata.y = event.y
        pendata.fclick = True
    else:
        canvas.create_line(pendata.x, pendata.y, event.x, event.y)
        pendata.x = event.x
        pendata.y = event.y

    pendata.list = pendata.list + [pendata.x]
    pendata.list = pendata.list + [pendata.y]

    print(pendata.list)


def send_information(pendata, multiplier_box, speed_box, mqtt_client):
    multiplier = multiplier_box.get()
    speed = speed_box.get()
    mqtt_client.send_message('multiplier_setup', [multiplier])
    mqtt_client.send_message('speed_setup', [speed])
    mqtt_client.send_message('coordinate_setup', [pendata.list])


def reset_coordinates(canvas, pendata):
    canvas.delete("all")
    pendata.fclick = False
    pendata.mouse_x = None
    pendata.mouse_y = None
    pendata.list = []


def switch_controls(canvas, label1, label2, label3, label4, multiplier_box, spin_box, speed_box, button, fix_button,
                    resetbutton, controller_button, checkbox, pendata):
    canvas.grid_forget()
    label1.grid_forget()
    label2.grid_forget()
    label3.grid_forget()
    label4.grid_forget()
    multiplier_box.grid_forget()
    spin_box.grid_forget()
    speed_box.grid_forget()
    button.grid_forget()
    resetbutton.grid_forget()
    controller_button.grid_forget()
    fix_button.grid_forget()
    checkbox.grid_forget()

    if pendata.currentsetting == 'gui':
        label3.grid()
        speed_box.grid()
        label4.grid()
        spin_box.grid()
        controller_button.grid(pady=5)
        fix_button.grid(pady=10)
        reset_coordinates(canvas, pendata)
        pendata.currentsetting = 'controller'
    elif pendata.currentsetting == 'controller':
        label1.grid(pady=5)
        canvas.grid(pady=5)
        button.grid(pady=5)
        label2.grid()
        multiplier_box.grid()
        label3.grid()
        speed_box.grid()
        checkbox.grid()
        resetbutton.grid(pady=5)
        controller_button.grid(pady=5)
        pendata.currentsetting = 'gui'


def handle_go_forward(speed_box, mqtt_client, pendata):
    if pendata.currentsetting == 'controller':
        speed = speed_box.get()
        mqtt_client.send_message('go_forward', [speed])


def handle_go_backward(speed_box, mttq_client, pendata):
    if pendata.currentsetting == 'controller':
        speed = speed_box.get()
        mttq_client.send_message('go_backward', [speed])


def handle_spin_left(spin_box, mttq_client, pendata):
    if pendata.currentsetting == 'controller':
        degrees = spin_box.get()
        mttq_client.send_message('spin_left', [degrees])


def handle_spin_right(spin_box, mttq_client, pendata):
    if pendata.currentsetting == 'controller':
        degrees = spin_box.get()
        mttq_client.send_message('spin_right', [degrees])


def stop(mttq_client, pendata):
    if pendata.currentsetting == 'controller':
        mttq_client.send_message('stop')


def change_value(checkbutton_observer, mqtt_client):
    value = checkbutton_observer.get()
    mqtt_client.send_message('change_value', [value])


main()
