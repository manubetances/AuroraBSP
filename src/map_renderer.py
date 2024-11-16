# Map render will render levels we create in 2D.
# Not for the game, but for debugging purposes.
from settings import *

class MapRenderer:
    def __init__(self, engine):
        self.engine = engine
        #
        raw_segments = [seg.pos for seg in self.engine.level_data.raw_segments]
        self.x_min, self.y_min, self.x_max, self.y_max = self.get_bounds(raw_segments)
        #
        self.raw_segments = self.remap_array(raw_segments)
        #
        self.segments = self.remap_array(
            [seg.pos for seg in self.engine.bsp_builder.segments])
        self.counter = 0.0

    def draw(self):
        self.draw_raw_segments()
        self.draw_segments()
        self.draw_player()
        self.counter += 0.0005

    def draw_player(self):
        x0, y0 = p0 = self.remap_vec2(self.engine.bsp_traverser.cam_pos)
        rl.draw_circle_v((x0, y0), 10, rl.GREEN)

    def draw_segments(self, seg_color = rl.ORANGE):
        segments_ids = self.engine.bsp_traverser.segs_ids_to_draw

        # Add (render) the segments in the order the traverser 
        for seg_id in segments_ids[:int(self.counter) % (len(segments_ids) + 1)]:
            (x0, y0), (x1, y1) = p0, p1 = self.segments[seg_id]
            #
            rl.draw_line_v((x0, y0), (x1, y1), seg_color)
            self.draw_normal(p0, p1, seg_color)

            rl.draw_circle_v((x0, y0), 3, rl.WHITE)

    # Draw the normal (front face of the line) of the segment.
    def draw_normal(self, p0, p1, color, scale = 12):
        p10 = p1 - p0
        normal = normalize(vec2(-p10.y, p10.x))
        n0 = (p0 + p1) * 0.5
        n1 = n0 + normal * scale
        #
        rl.draw_line_v((n0.x, n0.y), (n1.x, n1.y), color)

    # Draw the raw segment, using its start and end point
    def draw_raw_segments(self):
        for p0, p1 in self.raw_segments:
            (x0, y0), (x1, y1) = p0, p1
            rl.draw_line_v((x0, y0), (x1, y1), rl.DARKGRAY) 

    # Remap segments
    def remap_array(self, arr: list[vec2]):
        return[(self.remap_vec2(p0), self.remap_vec2(p1)) for p0, p1 in arr]

    # Remap 2D vectors
    def remap_vec2(self, p: vec2):
        x = self.remap_x(p.x)
        y = self.remap_y(p.y)
        return vec2(x, y)

    # Remap X axis so the dimensions are the one set by (window width - offset)
    def remap_x(self, x, out_min = MAP_OFFSET, out_max = MAP_WIDTH):
        return (x - self.x_min) * (out_max - out_min) / (self.x_max - self.x_min) + out_min

    # Remap Y axis so the dimensions are the one set by (window height - offset)
    def remap_y(self, y, out_min = MAP_OFFSET, out_max = MAP_HEIGHT):
        return (y - self.y_min) * (out_max - out_min) / (self.y_max - self.y_min) + out_min

    @staticmethod
    def get_bounds(segments: list[tuple[vec2]]):
        inf = float('inf')
        x_min, y_min, x_max, y_max = inf, inf, -inf, -inf
        #
        for p0, p1 in segments:
            # X Axis
            x_min = p0.x if p0.x < x_min else p1.x if p1.x < x_min else x_min
            x_max = p0.x if p0.x > x_max else p1.x if p1.x > x_max else x_max
            # Y Axis
            y_min = p0.y if p0.y < y_min else p1.y if p1.y < y_min else y_min
            y_max = p0.y if p0.y > y_max else p1.y if p1.y > y_max else y_max
        #
        return x_min, y_min, x_max, y_max
    