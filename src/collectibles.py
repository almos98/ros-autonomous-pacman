#!/usr/bin/env python
import rospy
from gazebo_msgs.srv import DeleteModel, SpawnModel
from geometry_msgs.msg import Pose

spawn_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)

MODEL_PATH = '/my_ros_data/catkin_ws/src/ros_autonomous_pacman/models/TESTCYLINDER/TESTCYLINDER.urdf'
COLLECTIBLE_NAME = 'Collectible_%s_%s'

# Takes floats x and y and spawns a model at that position.
# x and y are in WORLD coordinates.
def spawn_collectible(x, y, model_name=None):
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
def delete_collectible(x, y, model_name=None):
    if model_name is None:
        model_name = COLLECTIBLE_NAME % (x, y)
    
    print(model_name)
    resp = delete_model(
        model_name=model_name
    )

    if not resp.success:
        print("Error: %s" % resp.status_message)