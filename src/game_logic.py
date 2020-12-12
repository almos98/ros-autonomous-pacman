#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32

import collectibles
from grid import GridCoords

class GameLogic:
    def __init__(self):
        rospy.init_node("GameLogic")

        # Game State
        # 0 = Initializing
        # 1 = Running
        # 2 = Success (Pacman got all collectibles)
        # 3 = Game over (Pacman got eaten by a ghost)
        self.game_state = 0
        self.state_cb = [self.STATE_init, self.STATE_run]
        self.game_state_pub = rospy.Publisher("game_logic/state", Int32, queue_size=1)

        self.grid = None
        self.collectibles = set()
        self.collectible_count = 0
        

    def STATE_init(self):
        rospy.loginfo_once("Setting up the game.")
        
        self.grid = GridCoords.get_grid(grid_size_x=9, grid_size_y=12, offset_f = lambda x: (-(3 * x), -(6 * x)))
        exclude = set([(0,0), (0,1), (0,11), (1,0), (1,1), (1,11), (2,0), (2,11), (3,11), (4,11), (5,11), (8,0), (8,4), (8,5),(8,10), (8,11)])
        print(exclude)
        for x in range(self.grid.size_x):
            for y in range(self.grid.size_y):
                if (x, y) in exclude:
                    continue
                
                self.collectibles.add((x,y))
                (x_, y_) = self.grid.to_world_coords(x,y)
                collectibles.spawn(x_, y_, model_name="Collectible_%s_%s" % (x_, y_))
        
        self.collectible_count = len(self.collectibles)
        self.change_state(1)
            

    def STATE_run(self):
        rospy.loginfo_throttle(1, "Collectibles left: %s, Score: %s" % (len(self.collectibles), self.score()))

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