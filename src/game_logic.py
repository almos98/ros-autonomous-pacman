#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
from nav_msgs.msg import Odometry

import collectibles
from grid import GridCoords

class GameLogic:
    def __init__(self):
        rospy.init_node("GameLogic")

        # Game State
        # 0 = Initializing
        # 1 = Running
        # 2 = Game Over (win or loss)
        self.game_state = 0
        self.state_cb = [self.STATE_init, self.STATE_run, self.STATE_end]
        self.game_state_pub = rospy.Publisher("game_logic/state", Int32, queue_size=1)
        self.pacman_pos_sub = rospy.Subscriber("pacman/odom", Odometry, self.pacman_odom_cb)

        self.grid = None
        self.collectibles = set()
        self.collectible_count = 0
        self.pacman_pos = (0,0)
        

    def STATE_init(self):
        rospy.loginfo_once("Setting up the game.")
        
        self.grid = GridCoords.get_grid(grid_size_x=9, grid_size_y=12, offset_f = lambda x: (-(3 * x), -(6 * x)))
        # exclude = set([(0,0), (0,1), (0,11), (1,0), (1,1), (1,11), (2,0), (2,11), (3,11), (4,11), (5,11), (8,0), (8,4), (8,5),(8,10), (8,11)])
        include = set([(7,6),(7,7),(7,8),(6,7)])
        for x in range(self.grid.size_x):
            for y in range(self.grid.size_y):
                if (x, y) not in include:
                    continue
                
                self.collectibles.add((x,y))
                (x_, y_) = self.grid.to_world_coords(x,y)
                collectibles.spawn(x_, y_, model_name="Collectible_%s_%s" % (x, y))
        
        self.collectible_count = len(self.collectibles)
        self.change_state(1)


    def STATE_run(self):
        pacman_cell = self.grid.to_grid_coords(self.pacman_pos[0], self.pacman_pos[1])

        if pacman_cell in self.collectibles:
            self.collectibles.remove(pacman_cell)
            collectibles.delete(pacman_cell[0], pacman_cell[1])

            if len(self.collectibles) == 0:
                self.change_state(2)
        
        rospy.loginfo_throttle(1, "Collectibles left: %s, Score: %s" % (len(self.collectibles), self.score()))
        
    def STATE_end(self):
        rospy.loginfo_once("You won!" if len(self.collectibles) == 0 else "You lose!")
    
    def pacman_odom_cb(self, data):
        pos = data.pose.pose.position
        self.pacman_pos = (pos.x, pos.y)
    
    def score(self):
        return self.collectible_count - len(self.collectibles)
        
    def change_state(self, state):
        self.game_state = state
        self.game_state_pub.publish(state)

    def update(self):
        self.state_cb[self.game_state]()

        rospy.loginfo_throttle(1, "Game state is %s." % (self.game_state))

if __name__ == "__main__":
    game_logic = GameLogic()

    rate = rospy.Rate(10)
    # Wait for simulator
    while rospy.Time.now().to_sec() == 0:
        rate.sleep()

    while not rospy.is_shutdown():
        game_logic.update()
        rate.sleep()