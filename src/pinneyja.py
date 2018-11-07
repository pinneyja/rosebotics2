"""
  Capstone Project.  Code written by PUT_YOUR_NAME_HERE.
  Fall term, 2018-2019.
"""

import rosebotics_new as rb
import time
import random
import rosegraphics as rg
import math


def main():
    """ Runs YOUR specific part of the project """
    run_test_black_line = False
    run_test_arm_claw = False
    run_test_arm_claw_advanced = False
    run_test_final_project = False
    run_localized_final_tests = True

    if False:
        robot = rb.Snatch3rRobot()

    # Test follow black line function
    if run_test_black_line:
        follow_black_line(robot, False)

    # Test raise arm and close claw & calibrate methods
    if run_test_arm_claw:
        robot.arm.raise_arm_and_close_claw()
        robot.arm.calibrate()

    # Test move arm to position functions
    if run_test_arm_claw_advanced:
        robot.arm.move_arm_to_position(5112)
        robot.arm.move_arm_to_position(0)
        robot.arm.move_arm_to_position(3000)
        robot.arm.move_arm_to_position(0)

    if run_test_final_project:
        run_final_project(robot)

    if run_localized_final_tests:
        draw_sonar_image(random_method())


def random_method():
    seq = []
    for k in range(0,360,10):
        seq.append([k,random.randint(20,30)])
    return seq


def run_final_project(robot):
    results = perform_sonar_scan(robot)
    draw_sonar_image(results)
    pass


def perform_sonar_scan(robot):
    return robot.drive_system.spin_in_place_degrees(360, collect_sonar=True, robot=robot)


def draw_sonar_image(seq_of_seq):
    # 96 pixels in 1 inch
    x_width = 700  # width of RoseGraphics window
    y_height = 700  # height of RoseGraphics window
    scale = 10  # scale of real inches to screen inches; if 10, then 5 real inches translates to .5 screen inches
    window = rg.RoseWindow(x_width, y_height)
    # p_origin = rg.Point(500, 500)
    p_origin = rg.Point(x_width/2, y_height/2)
    p_origin.fill_color = "red"
    p_origin.outline_thickness = 10
    p_origin.attach_to(window)
    points = []
    for seq in seq_of_seq:
        degrees = (seq[0] / 360) * 2 * math.pi
        distance = (seq[1] * 96) / scale
        x_position = (x_width / 2) + distance * math.cos(degrees)
        y_position = (y_height / 2) + distance * math.sin(degrees)
        point = rg.Point(x_position, y_position)
        points.append(point)
    for point in points:
        point.outline_thickness = 5
        point.attach_to(window)
        window.render()
    for k in range(len(points)):
        if k == len(points) - 1:
            line = rg.Line(points[k], points[0])
        else:
            line = rg.Line(points[k], points[k+1])
        line.color = "gray"
        line.attach_to(window)
        window.render()
    window.close_on_mouse_click()


def follow_black_line(robot, is_counterclockwise):
    if is_counterclockwise:
        value = -1
    else:
        value = 1
        # isCounterclockwise == True then robot is turning left
        # else                                  is turning right
        # assumes robot is placed on black line to start

    color = rb.Color.BLACK.value
    while True:
        robot.drive_system.start_moving(30, 30)
        if robot.color_sensor.get_color() != color:
            robot.drive_system.stop_moving()
            while True:
                robot.drive_system.spin_in_place_degrees(value)
                if robot.color_sensor.get_color() == color:
                    break


main()
