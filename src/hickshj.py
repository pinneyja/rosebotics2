"""
  Capstone Project.  Code written by PUT_YOUR_NAME_HERE.
  Fall term, 2018-2019.
"""

import rosebotics as rb
import time


def main():
    """ Runs YOUR specific part of the project """
    run_test_ngon()


def run_test_ngon():
    print('should make triangle')
    ngon(3, 10)


#    print('should make square')
#    ngon(4, 10)

#    print('should be pentagon')
#    ngon(5, 5)


def ngon(sides, side_length):
    bot = rb.Snatch3rRobot()
    degrees = 360 / sides
    for k in range(side_length):
        bot.drive_system.go_straight_inches(side_length)
        bot.drive_system.spin_in_place_degrees(degrees)


main()
