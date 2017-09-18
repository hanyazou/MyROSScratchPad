#!/usr/bin/env python

import rospy
from monster_moto_shield import monster_moto_shield
from geometry_msgs.msg import Twist

class node():
    TREAD = 0.118  # distance between tracks in m
    def __init__(self):
        self.mms = monster_moto_shield()

    def cb_twist(self, msg):
        print msg
        cmd_vel = msg
        r_speed = cmd_vel.linear.x + cmd_vel.angular.z*self.TREAD/2
        l_speed = cmd_vel.linear.x - cmd_vel.angular.z*self.TREAD/2
        r_speed /= 1000
        l_speed /= 1000
        print l_speed, r_speed
        if r_speed < 0:
            self.mms.start(self.mms.RIGHT, self.mms.BACKWARD, -r_speed)
        else:
            self.mms.start(self.mms.RIGHT, self.mms.FORWARD, r_speed)
        if l_speed < 0:
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
