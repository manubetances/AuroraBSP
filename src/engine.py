from settings import *
from level_data import LevelData
from map_renderer import MapRenderer
from bsp.bsp_builder import BSPTreeBuilder
from bsp.bsp_traverser import BSPTreeTraverser

class Engine:
    def __init__(self, app):
        self.app = app
        #
        self.level_data = LevelData(self)   # Level Data
        self.bsp_builder = BSPTreeBuilder(self) # 
        self.bsp_traverser = BSPTreeTraverser(self) # Traverse the BSP Tree
        # Render 2D map for debugging
        self.map_renderer = MapRenderer(self)

    # Called in every frame of the game
    def update(self):
        self.bsp_traverser.update()

    # Draw 2D figures/objects
    def draw_2D(self):
        self.map_renderer.draw()

    # Draw 3D figures/objects
    def draw_3D(self):
        pass

    # Draw/Display on the window
    def draw(self):
        rl.begin_drawing()
        #Clear in each frame
        rl.clear_background(rl.BLACK)
        self.draw_3D()  # Render 3D stuff
        self.draw_2D()  # Render 2D stuff
        # End loop
        rl.end_drawing()
        