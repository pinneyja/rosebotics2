"""
  Capstone Project.  Code written by PUT_YOUR_NAME_HERE.
  Fall term, 2018-2019.
"""

import rosebotics_new as rb
import time


def main():
    """ Runs YOUR specific part of the project """
    run_test_black_line = False
    run_test_arm_claw = False
    run_test_arm_claw_advanced = False
    run_test_final_project = False

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


def run_final_project(robot):
    perform_sonar_scan(robot)
    pass


def perform_sonar_scan(robot):

    return robot.drive_system.spin_in_place_degrees(360, collect_sonar=True, robot=robot)


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
