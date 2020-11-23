#!/usr/bin/env python
import rospy, tf
from gazebo_msgs.srv import DeleteModel, SpawnModel
from geometry_msgs.msg import *

if __name__ == '__main__':
    print("Waiting for gazebo services...")
    spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', DeleteModel)
    spawn_model_client(
    model_name='TESTCYLINDER'
    )
    print("deleted")