#!/usr/bin/env python
import rospy
import sys
import math
import tf
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion



def scan_cb(msg):
   global state
   rangesInFront = msg.ranges[:45] + msg.ranges[314:] 
   # these are the degrees that will detect an object 
   if min(rangesInFront) <= .2:
      state = 'x'

def odometryCb(msg):
    #establishing global variable from callBack to be used else where
    global msgObj
    global getThereDistance
    global x,y,z 
    global yaw
    msgObj = msg.pose.pose.orientation
    getThereDistance = msg.pose.pose.position.x
    zPosition = msgObj.z
    quat = (msgObj.x, msgObj.y, msgObj.z, msgObj.w)
    #create a list of the orientation coordinates 
    roll,pitch,yaw = euler_from_quaternion(quat)  
    print yaw 


def key_cb(msg):
   global state; global last_key_press_time;global linear_component;global angular_component
   state = msg.data
   last_key_press_time = rospy.Time.now()
#    if state in key_mapping.keys():
#       linear_component , angular_component = key_mapping[state]

def print_state():
   print("---")
   print("STATE: " + state)
   # calculate time since last key stroke
   time_since = rospy.Time.now() - last_key_press_time
   print("SECS SINCE LAST KEY PRESS: " + str(time_since.secs))

 

def north():
    desired = 3.14
    t = Twist()
    if yaw > desired - tolerance and yaw < desired + tolerance:
        # print (yaw > desired - tolerance and yaw < desired + tolerance)
        t.linear.x = .22
    elif yaw == desired * 2:
        t.linear.x = 0     
    else:
        # hitting here off the bat 
        t.angular.z = directionToTurn(desired)
        #.2

    cmd_vel_pub.publish(t)


     
def west():
    desired = (3*math.pi)/2
    t = Twist()
    if yaw > desired - tolerance and yaw < desired + tolerance:
        t.linear.x = .22
    else:
        t.angular.z = .2
    cmd_vel_pub.publish(t)


def east():
    desired = math.pi/2
    t = Twist()
    if yaw > desired - tolerance and yaw < desired + tolerance:
        t.linear.x = .2
    else:
        t.angular.z = .2
    cmd_vel_pub.publish(t)


def south():
    desired = 0
    t = Twist()
    if yaw > desired - tolerance and yaw < desired + tolerance:
        t.linear.x = .2
    else:
        t.angular.z = .1
    cmd_vel_pub.publish(t)

def halt():
    t = Twist()
    cmd_vel_pub.publish(t)

def directionToTurn(desired):
    if(yaw < desired):
        print yaw + "is the yaw"
        return .5
    else:
        return -.5

# init node
rospy.init_node('test')
# subscribers/publishers
scan_sub = rospy.Subscriber('/scan', LaserScan, scan_cb)
# RUN rosrun prrexamples key_publisher.py to get /keys

# PUBLISHING TO /pacman/PUBLISHER due to name spacing 
key_sub = rospy.Subscriber('keys', String, key_cb)
rospy.Subscriber('/pacman/odom',Odometry,odometryCb)
cmd_vel_pub = rospy.Publisher('/pacman/cmd_vel', Twist, queue_size=10)
# start in state halted and grab the current time
state = "x"
last_key_press_time = rospy.Time.now()
# set rate
rate = rospy.Rate(10)
difference = rospy.Time.now()
stop = True
tolerance = .2
yaw = 0

key_mapping = { 'w': north, 'd': east,
                'a': west, 's': south,
                'x': halt }

# Wait for published topics, exit on ^c
while not rospy.is_shutdown():
    print state
    direction = key_mapping.get(state)
    direction()
    #print_state()
    # run at 10hz
    rate.sleep()