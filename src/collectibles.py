#!/usr/bin/env python
import rospy
from gazebo_msgs.srv import DeleteModel, SpawnModel, SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose

spawn_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

MODEL_PATH = '/my_ros_data/catkin_ws/src/ros_autonomous_pacman/models/TESTCYLINDER/TESTCYLINDER.urdf'
COLLECTIBLE_NAME = 'Collectible_%s_%s'

# Takes floats x and y and spawns a model at that position.
# x and y are in WORLD coordinates.
def spawn(x, y, model_name=None):
    if model_name is None:
        model_name = COLLECTIBLE_NAME % (x, y)

    pose = Pose()
    pose.position.x = x
    pose.position.y = y
    resp = spawn_model(
        model_name=model_name,
        model_xml=open(MODEL_PATH, 'r').read(),
        initial_pose=pose,
        reference_frame='world'
    )

    if not resp.success:
        print("Error: %s" % resp.status_message)

# Takes floats x and y and deletes the model at that position.
# x and y are in WORLD coordinates.
def delete(x, y, model_name=None):
    if model_name is None:
        model_name = COLLECTIBLE_NAME % (x, y)
    
    msg = ModelState()
    msg.model_name = model_name
    msg.pose.position.x = x
    msg.pose.position.y = -100
    msg.pose.position.z = y
    msg.pose.orientation.x = 0
    msg.pose.orientation.y = 0
    msg.pose.orientation.z = 0
    msg.pose.orientation.w = 0

    resp = set_state(msg)
    if not resp.success:
        print("Error: %s" % resp.status_message)
        
    # The code below doesn't work due to Gazebo issues.
    # resp = delete_model(
    #     model_name=model_name
    # )
