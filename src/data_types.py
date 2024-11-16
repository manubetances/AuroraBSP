from settings import *

# Segments: 
class Segment:
    def __init__(self, p0: tuple[float], p1: tuple[float]):
        #
        self.pos: tuple[vec2] = vec2(p0), vec2(p1)
        self.vector: vec2 = self.pos[1] - self.pos[0]

class BSPNode:
    def __init__(self):
        #
        self.front: BSPNode = None
        self.back: BSPNode = None
        #
        self.splitter_p0: vec2 = None
        self.splitter_p1: vec2 = None
        self.splitter_vec: vec2 = None
        # Each Node instance has its unique identifier
        self.segment_id: int = None
