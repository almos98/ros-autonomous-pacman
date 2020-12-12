#!/usr/bin/env python

from math import floor

# METERS_PER_PIXEL = 0.05
# CELL_SIZE_IN_PIXELS = 24
# CELL_SIZE_IN_METERS = CELL_SIZE_IN_PIXELS * METERS_PER_PIXEL
# OFFSET_X = -(3 * CELL_SIZE_IN_METERS)
# OFFSET_Y = -(6 * CELL_SIZE_IN_METERS)
# GRID_SIZE_X = 9
# GRID_SIZE_Y = 12

# # Takes grid coordinates x and y and returns the transformed coordinates into world coordinates.
# def to_world_coords(x, y):
#     x = OFFSET_X + (x * CELL_SIZE_IN_METERS)
#     y = OFFSET_Y + (y * CELL_SIZE_IN_METERS)

#     return (x, y)

# if __name__ == "__main__":
#     from collectibles import spawn_collectible, delete_collectible
#     # (x, y) = to_world_coords(0,0)
#     # print(x,y)
#     # spawn_collectible(x, y)
#     for x in range(GRID_SIZE_X):
#         for y in range(GRID_SIZE_Y):
#             (x_, y_) = to_world_coords(x,y)
#             print("%s -> %s, %s -> %s" % (x, x_, y, y_))
#             spawn_collectible(x_, y_, model_name="Collectible_%s_%s" % (x, y))

#     # delete_collectible(0, 0)

class GridCoords:
    __grid = None
    @staticmethod
    def get_grid(grid_size_x=0, grid_size_y=0, offset_f=lambda x: (0,0), meters_per_pixel = 0.05, cell_size_px = 24):
        if GridCoords.__grid == None:
            GridCoords(grid_size_x, grid_size_y, offset_f, meters_per_pixel = meters_per_pixel, cell_size_px = cell_size_px)
        return GridCoords.__grid
    
    # Default constructor
    # grid_size_x: Number of horizontal cells
    # grid_size_y: Number of vertical cells
    # offset_f: Lambda function to calculate (x,y) offset of the grid
    def __init__(self, grid_size_x, grid_size_y, offset_f, meters_per_pixel = 0.05, cell_size_px = 24):
        if GridCoords.__grid != None:
            raise Exception("Singleton is already constructed")
        
        self.cell_size_m = meters_per_pixel * cell_size_px
        self.offset = offset_f(self.cell_size_m)
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y

        GridCoords.__grid = self

    # Takes grid coordinates x and y and returns the transformed coordinates into world coordinates.
    def to_world_coords(self, x, y):
        x = self.offset[0] + (x * self.cell_size_m)
        y = self.offset[1] + (y * self.cell_size_m)

        return (x, y)