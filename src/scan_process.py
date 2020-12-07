#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
#from ros_autonomous_pacman.msg import ProcessedScan

class ScanProcess:
    def __init__(self):
        rospy.init_node("ScanProcessor")

        self.scan_sub = rospy.Subscriber('pacman/scan', LaserScan, self.scan_cb)
        self.odom_sub = rospy.Subscriber('pacman/odom', Odometry, self.odom_cb)

        self.scan_data = None
        self.odom_data = None
        
        # self.pub = rospy.Publisher('pacman/scan/processed', ProcessedScan, queue_size=1)

    def scan_cb(self, data):
        self.scan_data = data

    def odom_cb(self, data):
        self.odom_data = data

    def update(self):
        # Process scan and odom data
        # Build message
        # Publish
        pass

if __name__ == "__main__":
    process = ScanProcess()

    rate = rospy.Rate(10)
    # Wait for simulator
    while rospy.Time.now().to_sec() == 0:
        rate.sleep()

    while not rospy.is_shutdown():
        process.update()
        rate.sleep()
