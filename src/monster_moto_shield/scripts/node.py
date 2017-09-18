#!/usr/bin/env python

import rospy
import math
from monster_moto_shield import monster_moto_shield
from geometry_msgs.msg import Twist

class node():
    TREAD = 0.118  # distance between tracks in m
    def __init__(self):
        self.mms = monster_moto_shield()

    def cb_twist(self, msg):
        # print msg
        cmd_vel = msg
        linear = cmd_vel.linear.x / -23000
        angular = cmd_vel.angular.z / -23000
        r_speed = linear + angular*self.TREAD/2 * 20
        l_speed = linear - angular*self.TREAD/2 * 20
        print '%5.2f %5.2f' % (l_speed, r_speed)
        if abs(r_speed) < 0.1:
            self.mms.stop(self.mms.RIGHT)
        elif r_speed < 0:
            self.mms.start(self.mms.RIGHT, self.mms.BACKWARD, -r_speed)
        else:
            self.mms.start(self.mms.RIGHT, self.mms.FORWARD, r_speed)

        if abs(l_speed) < 0.1:
            self.mms.stop(self.mms.LEFT)
        elif l_speed < 0:
            self.mms.start(self.mms.LEFT, self.mms.BACKWARD, -l_speed)
        else:
            self.mms.start(self.mms.LEFT, self.mms.FORWARD, l_speed)

    def setup(self):
        rospy.init_node('monster_moto_shield')
        rospy.Subscriber('/cmd_vel', Twist, self.cb_twist)


if __name__ == '__main__':
    n  = node()
    try:
        n.setup()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
