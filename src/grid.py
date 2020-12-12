#!/usr/bin/env python

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
        self.size_x = grid_size_x
        self.size_y = grid_size_y

        GridCoords.__grid = self

    # Takes grid coordinates x and y and returns the world coordinates.
    def to_world_coords(self, x, y):
        x = self.offset[0] + (x * self.cell_size_m)
        y = self.offset[1] + (y * self.cell_size_m)

        return (x, y)

    # Takes world coordinates x and y and returns the transformed coordinates.
    def to_grid_coords(self, x, y):
        x = int((round(x) - self.offset[0]) / self.cell_size_m)
        y = int((round(y) - self.offset[1]) / self.cell_size_m)
        return (x, y)