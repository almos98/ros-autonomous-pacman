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

        self.init_time = 10000
        self.STATE_init(from_init=True)

        self.grid = None
        

    def STATE_init(self, from_init=False):
        rospy.loginfo_once("Setting up the game.")

        if not from_init:
            self.init_time -= 1
            return

        self.grid = GridCoords.get_grid(grid_size_x=9, grid_size_y=12, offset_f = lambda x: (-(3 * x), -(6 * x)))


        

    def STATE_run(self):
        print("lmao")

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