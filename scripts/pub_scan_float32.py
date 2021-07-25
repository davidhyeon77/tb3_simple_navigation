#!/usr/bin/env python
#-*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32


class Scanning:
    def __init__(self):
        rospy.init_node('scanning', anonymous = True)
        rospy.Subscriber('/scan', LaserScan, self.check_target)
        self.pub = rospy.Publisher('/dist_scan', Float32, queue_size = 10)
        self.min_ranges = 0

    def check_target(self, msg):
        t1 = msg.ranges
        min_range = min(i for i in t1 if i > 0.05)
        min_index = t1.index(min_range)

        if min_index > 80 and min_index < 280:
            pass
        else:
            self.min_range = min_range
            print(round(self.min_range,4))
        
        p = Float32()
        p = min_range
        self.pub.publish(p)    

if __name__ == '__main__':
    try:
        Scanning()
        rospy.spin()
        
    except rospy.ROSInterruptException:  pass
