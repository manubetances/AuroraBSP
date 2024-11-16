import pyray as rl
import glm
from glm import vec2, vec3, ivec2, normalize, cross, dot, atan2, sin, cos, length

# Initial Settings of the Game

WIN_RESOLUTION = WIN_WIDTH, WIN_HEIGHT = 1600, 900  # Resolution

MAP_OFFSET = 50
MAP_WIDTH, MAP_HEIGHT = WIN_WIDTH - MAP_OFFSET, WIN_HEIGHT - MAP_OFFSET

#
EPS = 1e-4

