"""
  Capstone Project.  Code written by Hunter Hicks.
  Fall term, 2018-2019.
"""

import rosebotics_new as rb
import ev3dev.ev3 as ev3


def main():
    """ Runs YOUR specific part of the project """
    #    run_test_ngon()
    distance_beep()


def run_test_ngon():
    print('should make triangle')
    ngon(3, 10)

    print('should make square')
    ngon(4, 10)

    print('should be pentagon')
    ngon(5, 5)


def ngon(sides, side_length):
    bot = rb.Snatch3rRobot()
    degrees = 360 / sides
    for k in range(sides):
        bot.drive_system.go_straight_inches(side_length)
        bot.drive_system.spin_in_place_degrees(degrees)


def distance_beep():
    sensor = rb.InfraredAsProximitySensor('in4')
    while True:
        d = sensor.get_distance_to_nearest_object_in_inches()
        if 11 <= d <= 13:
            ev3.Sound.beep().wait()
            print(d)
            break


main()
