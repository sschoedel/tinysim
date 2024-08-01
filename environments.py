import visualizer

import numpy as np

class DefaultEnvironment():
    def __init__(self, ground_height=0.0):
        self.ground_height = ground_height
        self.artist = visualizer.LineArtist(1)
    
    def calculate_lines_start_end(self):
        self.p1 = np.array([-100, 0])
        self.p2 = np.array([100, 0])
        return np.array([self.p1, self.p2])
    
    def draw(self, world_to_window_coord_transform, world_to_window_scale):
        self.artist.draw(self.calculate_lines_start_end(), world_to_window_coord_transform, world_to_window_scale)