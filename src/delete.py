#!/usr/bin/env python
import rospy, tf
from gazebo_msgs.srv import DeleteModel, SpawnModel
from geometry_msgs.msg import *

if __name__ == '__main__':
    print("Waiting for gazebo services...")
    delete_model_client = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
    delete_model_client(
    model_name='TESTCYLINDER'
    )
    print("deleted")