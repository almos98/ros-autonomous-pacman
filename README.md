# ros_autonomous_pacman

[Lab notebook contribution](https://campus-rover.gitbook.io/lab-notebook/faq/sdf_to_urdf)

## Introduction
Pacman is placed in a map with virtual collectibles and the goal is for pacman to get all collectibles without crashing into any of the "ghost" robots.

## What was created
1. Imported map and models to be used for the game.
2. Grid coordinate system for higher level control and simple collision detection.
3. Dynamic manipulation of Gazebo models.
4. Pacman game logic in ROS.

### Grid-based Movement
Pacman is a very old game and its design was influenced by its age: grid-based movement. To achieve this in ROS, a custom coordinate system was implemented that maps world coordinates to a grid. The second challenge of this algorithm was having absolute controls; 'w' always makes pacman move north, 'd' always makes pacman move east, etc.

This is accomplished by getting wall directions relative to the robot and then transforming them based on odometry data from the robot. Another important part of replicating pacman movement is that it only moves in a direction with no walls. This is more relevant when combined with move_base, because it could take a path to the position the controller feeds it, instead of not moving.

Similarly, the virtual collectibles also rely on the coordinate system to be placed on the map and to detect when pacman has collected them. Making use of the fact that the world to grid coordinate conversion is a surjective function.

### Pivots
1. Gazebo services can hang/timeout and be unreliable (deleting models namely) so instead of deleting models we have to move them somewhere not visible to the camera.
2. We found the grid-based movement controller more interesting to work on than the autonomous controller for pacman, so we worked on that instead.

## Reflection
We both liked working together on this project and the workload was assigned to reflect our personal interests. Alexion focused on grid coordinate system and game logic while Ilan focused on map creation, Gazebo manipulation through code and controller. We were too broad with our original idea and thought we would have enough time to implement full autonomy. Thus we had to trade off some autonomy to stay true to pacman's roots. We also underestimated how hard it was to have multiple robots functioning under the same system correctly.

## Execution
To run the game itself use:
```
$ roslaunch ros_autonomous_pacman pacman.launch
```

To launch the manual controller run the following commands (on separate terminals):
```
$ rosrun ros_autonomous_pacman teleop.py
$ rosrun prrexamples key_publisher.py 
```

## Useful links for this project
- [Maps Repo](https://github.com/tu-darmstadt-ros-pkg/hector_nist_arenas_gazebo)
- [SDF to URDF converter](https://github.com/andreasBihlmaier/pysdf)
- [SDF to URDF video](https://www.youtube.com/watch?v=8g5nMxhi_Pw)
