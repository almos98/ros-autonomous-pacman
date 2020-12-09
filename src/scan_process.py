#!/usr/bin/env python
import math
import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from ros_autonomous_pacman.msg import ProcessedScan
from tf.transformations import euler_from_quaternion

MIN_RANGE = .2
# Class for processing Lidar and Odom data 
class ScanProcess:
    def __init__(self):
        rospy.init_node("ScanProcessor")

        self.scan_sub = rospy.Subscriber('pacman/scan', LaserScan, self.scan_cb)
        self.odom_sub = rospy.Subscriber('pacman/odom', Odometry, self.odom_cb)

        self.scan_data = None

        self.yaw = None
        self.pub = rospy.Publisher('pacman/scan/processed', ProcessedScan, queue_size=1)

    ########################
    # Subscriber Callbacks #
    ########################

    def scan_cb(self, data):
        self.scan_data = data

    def odom_cb(self, data):
        # if data is None:
        #     return
        quat = data.pose.pose.orientation
        #create a list of the orientation coordinates 
        self.yaw = euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])[2]  
        

    ########################
    # Processing Function #
    ########################

    def update(self):
        if self.scan_data is None or self.yaw is None:
            return
        # Process scan and odom data
        # Build message
        # Publish
        # rangesNorth = self.scan_data.ranges[:30] + self.scan_data.ranges[330:] 
        # rangesEast = self.scan_data.ranges[54:124] 
        # rangesSouth = self.scan_data.ranges[165:195] 
        # rangesWest = self.scan_data.ranges[234:304] 
 

        processed_data = ProcessedScan()
        processed_data.facing = self.yaw
        n_index = -1
        pi = math.pi
        if self.yaw > (5 * pi)/6 and self.yaw < (7 * pi)/6: 
            # facing north  
            n_index = 0
            print n_index
        elif self.yaw > (pi)/3 and self.yaw < ( 2 * pi)/3: #
            n_index = 89
            print n_index
        elif self.yaw < (pi/6) and self.yaw > (11 * pi)/11: #
            n_index = 180
            print n_index
        elif self.yaw > (4 * pi)/3 and self.yaw < (5 * pi)/3: 
            n_index = 270
            print n_index
        elif n_index == -1:
            return

        processed_data.north = min(self.subset(self.scan_data.ranges,n_index)) <= MIN_RANGE
        processed_data.east = min(self.subset(self.scan_data.ranges, (n_index + 90) % 360)) <= MIN_RANGE
        processed_data.south = min(self.subset(self.scan_data.ranges,(n_index + 180) % 360)) <= MIN_RANGE
        processed_data.west = min(self.subset(self.scan_data.ranges,(n_index + 270) % 360)) <= MIN_RANGE

        self.pub.publish(processed_data)

    def subset(self,ranges, i, n=30):
        return [ranges[x] for x in range(i-n,i+n) if x >= self.scan_data.range_min]

# MAIN FUNCTION 
if __name__ == "__main__":
    process = ScanProcess()

    rate = rospy.Rate(10)
    # Wait for simulator
    while rospy.Time.now().to_sec() == 0:
        rate.sleep()

    while not rospy.is_shutdown():
        process.update()
        rate.sleep()
