from settings import *
from data_types import Segment, BSPNode
from utils import cross_2D
from copy import copy
import random
import multiprocessing as mp

class BSPTreeBuilder:
    def __init__(self, engine):
        self.engine = engine
        # Create BSP tree based on the raw segments of the map
        self.raw_segments = engine.level_data.raw_segments

        # Define Root node. This node contain all references of the BSP tree
        # The most important part of this engine
        self.root_node = BSPNode()
        #
        self.segments = [] # Segments created during BSP Tree Creation
        self.seg_id = 0

        # Optimizing rendering of segments
        seed = self.find_best_seed_mp()    # Generate best seed after map design is done
        #seed = self.engine.level_data.settings['seed']
        random.seed(seed)
        random.shuffle(self.raw_segments)

        #
        self.num_front, self.num_back, self.num_splits = 0, 0, 0
        self.build_bsp_tree(self.root_node, self.raw_segments)
        #

    # Find best seed using multithreading (its a very consuming task)
    def find_best_seed_mp(self, start_seed = 0, end_seed = 1_000_000):
        cpu_count = mp.cpu_count()
        return_dict = mp.Manager().dict()

        cpu_range = (end_seed - start_seed) // cpu_count
        procs = []

        for i in range(cpu_count):
            i_start_seed = i * cpu_range + start_seed
            i_end_seed = (i + 1) * cpu_range + start_seed
            print(f'cpu {i}: {i_start_seed}, {i_end_seed}')

            proc = mp.Process(
                target = self.find_best_seed,
                args=(i, i_start_seed, i_end_seed, return_dict)
            )
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        best_seed = min(return_dict.values(), key = lambda t: t[0])[1]
        print('\nBest Seed: ', best_seed)
        return best_seed
        
    # Find best seed when map is completely designed then add it to the settings of the map
    def find_best_seed (self, i_cpu, start_seed, end_seed, return_dict, weight_factor = 3):
        best_seed, best_score = -1, float('inf')

        for seed in range(start_seed, end_seed):
            raw_segments = self.raw_segments.copy()
            random.seed(seed)
            random.shuffle(raw_segments)

            # The lower the score of a seed the more optimal is the BSP tree
            root_node = BSPNode()
            self.segments = []
            self.seg_id = 0

            self.num_front, self.num_back, self.num_splits = 0, 0, 0
            self.build_bsp_tree(root_node, raw_segments)

            score = abs(self.num_back - self.num_front) + weight_factor * self.num_splits
            if score < best_score:
                best_seed, best_score = seed, score
            
            print('best_seed = ', best_seed, 'score = ', best_score)
            return_dict[i_cpu] = (best_score, best_seed)

    # Create BSP Tree
    def split_space(self, node: BSPNode, input_segments: list[Segment]):
        # Select first segment as the splitter
        splitter_seg = input_segments[0]
        splitter_pos = splitter_seg.pos
        splitter_vec = splitter_seg.vector

        node.splitter_vec = splitter_vec
        node.splitter_p0 = splitter_pos[0]
        node.splitter_p1 = splitter_pos[1]

        front_segments, back_segments = [], []

        for segment in input_segments[1:]:
            #
            segment_start = segment.pos[0]
            segment_end = segment.pos[1]
            segment_vector = segment.vector

            # Find the numerator and denominator
            numerator = cross_2D((segment_start - splitter_pos[0]), splitter_vec)
            denominator = cross_2D(splitter_vec, segment_vector)

            # if the denominator is zero (0) the lines are parallel
            denominator_is_zero = abs(denominator) < EPS

            # segments are collinear if they are parallel and the numerator is zero
            numerator_is_zero = abs(numerator) < EPS

            if denominator_is_zero and numerator_is_zero:
                front_segments.append(segment)
                continue

            if not denominator_is_zero:
                # Intersection point is the point on a line segment that divides it
                intersection = numerator / denominator

                # segments that are not parallel and t is in (0, 1) should be divided
                if 0.0 < intersection < 1.0:
                    # Count the number of splits in segments
                    self.num_splits += 1
                    #
                    intersection_point = segment_start + intersection * segment_vector

                    #
                    r_segment = copy(segment)
                    r_segment.pos = segment_start, intersection_point
                    r_segment.vector = r_segment.pos[1] - r_segment.pos[0]

                    l_segment = copy(segment)
                    l_segment.pos = intersection_point, segment_end
                    l_segment.vector = l_segment.pos[1] - l_segment.pos[0]

                    if numerator > 0:
                        l_segment, r_segment - r_segment, l_segment

                    front_segments.append(r_segment)
                    back_segments.append(l_segment)
                    continue

            if numerator < 0 or (numerator_is_zero and denominator > 0):
                front_segments.append(segment)

            elif numerator > 0 or (numerator_is_zero and denominator < 0):
                back_segments.append(segment)

        self.add_segment(splitter_seg, node)
        return front_segments, back_segments
    
    #
    def add_segment(self, splitter_seg: Segment, node: BSPNode):
        self.segments.append(splitter_seg)
        node.segment_id = self.seg_id

        self.seg_id += 1

    def build_bsp_tree(self, node: BSPNode, input_segments: list[Segment]):
        if not input_segments:
            return None
        #
        front_segments, back_segments = self.split_space(node, input_segments)

        if back_segments:
            self.num_back += 1

            node.back = BSPNode()
            self.build_bsp_tree(node.back, back_segments)

        if front_segments:
            self.num_front += 1

            node.front = BSPNode()
            self.build_bsp_tree(node.front, front_segments)