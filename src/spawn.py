#!/usr/bin/env python
import rospy, tf
from gazebo_msgs.srv import DeleteModel, SpawnModel
from geometry_msgs.msg import *

if __name__ == '__main__':
    print("Waiting for gazebo services...")
    spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
    spawn_model_client(
    model_name='TESTCYLINDER',
    model_xml=open('/my_ros_data/catkin_ws/src/ros-autonomous-pacman/models/TESTCYLINDER/TESTCYLINDER.urdf', 'r').read(), 
    initial_pose=Pose(),
    reference_frame='world'
    )
    print("SPAWNED")
    