from settings import *
from data_types import BSPNode
from utils import is_on_front

class BSPTreeTraverser:
    def __init__(self, engine):
        self.engine = engine
        self.root_node = engine.bsp_builder.root_node
        self.segments = engine.bsp_builder.segments

        # TEMPORARY DEBUG PURPOSE
        self.cam_pos = vec2(6, 7)
        self.segs_ids_to_draw = []

    def update(self):
        self.segs_ids_to_draw.clear()
        self.traverse(self.root_node)

    def traverse(self, node: BSPNode):
        if node is None:
            return None
        
        on_front = is_on_front(self.cam_pos - node.splitter_p0, node.splitter_vec)
        # The engine is based on traversing the BSP Tree from front to back
        
        # If the camera is on the front we recursively call this method
        # And put the segment ID in the list to render
        if on_front:
            self.traverse(node.front)
            self.segs_ids_to_draw.append(node.segment_id)
            self.traverse(node.back)
        # If the camera is behind the splitter we do the opposite
        else:
            self.traverse(node.back)
            self.segs_ids_to_draw.append(node.segment_id)
            self.traverse(node.front)