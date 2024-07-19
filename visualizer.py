import pyglet

class LineArtist():
    def __init__(self, num_lines):
        self.num_lines = num_lines
        self.line_widths = [10]*self.num_lines
        self.line_colors = [(255, 255, 255)]*self.num_lines
        self.line_batch = pyglet.graphics.Batch()
        self.lines = [None] * self.num_lines
    
    def draw(self, points_in_line, pixel_scale_func):
        assert len(points_in_line) > 1
        prev_point = points_in_line[0]
        for i, point in enumerate(points_in_line[1:]):
            prev_point_window = pixel_scale_func(prev_point[0], prev_point[1])
            point_window = pixel_scale_func(point[0], point[1])
            self.lines[i] = pyglet.shapes.Line(prev_point_window[0], prev_point_window[1],    # point 1 x, y
                                               point_window[0], point_window[1],              # point 2 x, y
                                               self.line_widths[i],
                                               self.line_colors[i],
                                               batch=self.line_batch) 
            prev_point = point
        self.line_batch.draw()   


class RobotVisualizer(pyglet.window.Window):
    def __init__(self, robot, window_width=1000, 
                              window_height=750, 
                              window_title="SCS3", 
                              pixels_per_meter=100):
        super().__init__(window_width, window_height, window_title)
        self.pixels_per_meter = pixels_per_meter
        self.world_origin_x = self.width / 2.0          # World origin x in window coordinates
        self.world_origin_y = self.height / 2.0         # World origin y in window coordinates
        self.robot = robot
    
    def world_to_window(self, x_world, y_world):
        '''Convert from world coordinates (x -> right, y -> up) to
            window coordinates (x -> right, y -> down)
        '''
        return (self.world_origin_x + x_world*self.pixels_per_meter, 
                self.world_origin_y + y_world*self.pixels_per_meter)
    
    def on_draw(self):
        self.clear()
        self.robot.draw(self.world_to_window)
    
    def start(self):
        pyglet.app.run() # blocks until window is closed