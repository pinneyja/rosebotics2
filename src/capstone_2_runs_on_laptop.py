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
import math
import rosegraphics as rg


def main():
    """ Constructs and runs a GUI for this program. """
    receiver = Receiver()
    controller = com.MqttClient(receiver)
    controller.connect_to_ev3()
    sender = Sender(controller)
    root = tkinter.Tk()
    setup_gui(root, sender)

    root.mainloop()


def setup_gui(root, controller):
    """ Constructs and sets up widgets on the given window. """
    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid()

    button = ttk.Button(main_frame, text="Execute Sonar Scan")
    button["command"] = lambda: controller.handle_sonar_scan()
    button.grid()
    text = ttk.Label(main_frame, text="Click anywhere on the window to use the arrow keys to navigate.", padding=10)
    text.grid()
    root.bind_all('<KeyPress>', lambda event: controller.handle_key_press(event))
    root.bind_all('<KeyRelease>', lambda event: controller.handle_key_release(event))

    # root.bind_all('<Key-Up>', lambda event: print("I'm up"))
    # root.bind_all('<Key-Down>', lambda event: print("I'm down"))
    # root.bind_all('<Key-Left>', lambda event: print("I'm left"))
    # root.bind_all('<Key-Right>', lambda event: print("I'm right"))

    # speed_entry_box = ttk.Entry(frame)
    # go_forward_button = ttk.Button(frame, text="Go forward")
    # stop_button = ttk.Button(frame, text="Stop")
    #
    # speed_entry_box.grid()
    # go_forward_button.grid()
    # stop_button.grid()
    #
    # go_forward_button['command'] = \
    #     lambda: handle_go_forward(speed_entry_box, sender_obj)
    # stop_button['command'] = \
    #     lambda: handle_stop(sender_obj)


class Receiver(object):
    def __init__(self):
        pass

    def sonar(self, dictionary):
        """
        :type dictionary: dictionary
        """
        seq_of_seq = dictionary
        # seq_of_seq = [[330, 20], [345, 19.31], [15, 19.31], [30, 20]]
        # for key in dictionary.keys():
        #     seq_of_seq.append([key, dictionary[key]])
        # 96 pixels in 1 inch
        x_width = 700  # width of RoseGraphics window
        y_height = 700  # height of RoseGraphics window
        scale = 8  # scale of real inches to screen inches; if 10, then 5 real inches translates to .5 screen inches
        window = rg.RoseWindow(x_width, y_height)
        # p_origin = rg.Point(500, 500)
        p_origin = rg.Point(x_width / 2, y_height / 2)
        p_origin.fill_color = "red"
        p_origin.outline_thickness = 10
        p_origin.attach_to(window)
        # print(seq_of_seq)
        points = []
        for seq in seq_of_seq:
            print(seq)
            degrees = math.fabs(((float(seq[0])) / 360) * 2 * math.pi)
            distance = (seq[1] * 96) / scale
            x_position = (x_width / 2) + distance * math.sin(degrees)
            y_position = (y_height / 2) - distance * math.cos(degrees)
            distance_formula = math.sqrt((distance*math.sin(degrees))**2 + (distance*math.cos(degrees))**2)
            print(math.fabs(distance-distance_formula) < .5)
            point = rg.Point(x_position, y_position)
            # if 0 <= seq[0] < 90:
            #     point.outline_color = "red"
            # elif 90 < seq[0] < 180:
            #     point.outline_color = "blue"
            # elif 180 < seq[0] < 270:
            #     point.outline_color = "green"
            # elif 270 < seq[0] <= 360:
            #     point.outline_color = "yellow"
            points.append(point)
        for point in points:
            point.outline_thickness = 5
            point.attach_to(window)
            window.render()
        for k in range(len(points)):
            if k == len(points) - 1:
                line = rg.Line(points[k], points[0])
            else:
                line = rg.Line(points[k], points[k + 1])
            line.color = "gray"
            line.attach_to(window)
            window.render()
        window.close_on_mouse_click()


class Sender(object):
    def __init__(self, controller):
        self.up_is_pressed = False
        self.down_is_pressed = False
        self.left_is_pressed = False
        self.right_is_pressed = False
        self.left_stop_action = 0
        self.right_stop_action = 0
        self.controller = controller

    def handle_sonar_scan(self):
        self.controller.send_message("sonar", [360])

    def handle_key_press(self, event):  # Handles any key press events
        # print("Pressed", event.keysym)
        if event.keysym == "Up":
            self.up_is_pressed = True
        elif event.keysym == "Down":
            self.down_is_pressed = True
        elif event.keysym == "Left":
            self.left_is_pressed = True
        elif event.keysym == "Right":
            self.right_is_pressed = True
        self.handle_new_instructions()

    def handle_key_release(self, event):  # Handles any key release events
        # print("Released", event.keysym)
        if event.keysym == "Up":
            self.up_is_pressed = False
        elif event.keysym == "Down":
            self.down_is_pressed = False
        elif event.keysym == "Left":
            self.left_is_pressed = False
        elif event.keysym == "Right":
            self.right_is_pressed = False
        self.handle_new_instructions()

    def handle_new_instructions(self):  # Handles the change in key presses
        left_stop_action = self.left_stop_action
        right_stop_action = self.right_stop_action

        if self.up_is_pressed:
            left_stop_action = left_stop_action + 100
            right_stop_action = right_stop_action + 100
        if self.down_is_pressed:
            left_stop_action = left_stop_action - 200
            right_stop_action = right_stop_action - 200
        if self.left_is_pressed:
            left_stop_action = left_stop_action - 50
            right_stop_action = right_stop_action + 100
        if self.right_is_pressed:
            left_stop_action = left_stop_action + 100
            right_stop_action = right_stop_action - 50
        if left_stop_action % 100 != 0:
            if left_stop_action < 0:
                left_stop_action = -1 * (left_stop_action % 100)
            else:
                left_stop_action = left_stop_action % 100
        else:
            if left_stop_action < 0:
                left_stop_action = -100
            else:
                left_stop_action = 100
        if right_stop_action % 100 != 0:
            if right_stop_action < 0:
                right_stop_action = -1 * (right_stop_action % 100)
            else:
                right_stop_action = right_stop_action % 100
        else:
            if right_stop_action < 0:
                right_stop_action = -100
            else:
                right_stop_action = 100

        if (not self.up_is_pressed) & (not self.down_is_pressed) & \
           (not self.left_is_pressed) & (not self.right_is_pressed):
            left_stop_action = 0
            right_stop_action = 0
        # print("Sending: [{}, {}]".format(left_stop_action, right_stop_action))
        self.controller.send_message("go", [left_stop_action, right_stop_action])


# def handle_go_forward(entry_box, mqtt_obj):
#     """
#     Tells the robot to go forward at the speed specified in the given entry box.
#     """
#     speed_string = entry_box.get()
#     print("go_forward, value:", speed_string)
#     mqtt_obj.send_message("go_forward", [speed_string])
#
#
# def handle_stop(mqtt_obj):
#     mqtt_obj.send_message("stop", [])

main()
