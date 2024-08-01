import pyglet

class LineArtist():
    def __init__(self, num_lines, line_width=2, color=(255, 255, 255)):
        self.num_lines = num_lines
        self.line_widths = [line_width]*self.num_lines
        self.line_colors = [color]*self.num_lines
        self.line_batch = pyglet.graphics.Batch()
        self.lines = [None] * self.num_lines
    
    def draw(self, points_in_line, world_to_window_coord_transform, world_to_window_scale):
        assert len(points_in_line) > 1
        prev_point = points_in_line[0]
        for i, point in enumerate(points_in_line[1:]):
            prev_point_window = world_to_window_coord_transform(prev_point[0], prev_point[1])
            point_window = world_to_window_coord_transform(point[0], point[1])
            self.lines[i] = pyglet.shapes.Line(prev_point_window[0], prev_point_window[1],    # point 1 x, y
                                               point_window[0], point_window[1],              # point 2 x, y
                                               self.line_widths[i],
                                               self.line_colors[i],
                                               batch=self.line_batch) 
            prev_point = point
        self.line_batch.draw()  


class RectangleArtist():
    def __init__(self, width, line_width=2, color=(255, 255, 255)):
        self.width = width
        self.line_width = line_width
        self.color = color
        self.rectangle_batch = pyglet.graphics.Batch()
        self.rectangle = None
    
    def draw(self, x, y, width, height, rotation, world_to_window_coord_transform, world_to_window_scale):
        xy_window = world_to_window_coord_transform(x, y)
        width_window = world_to_window_scale(width)
        height_window = world_to_window_scale(height)
        self.rectangle = pyglet.shapes.Rectangle(xy_window[0], xy_window[1],
                                                 width_window, height_window,
                                                 color=self.color,
                                                 batch=self.rectangle_batch)
        self.rectangle_batch.draw()


class RobotVisualizer(pyglet.window.Window):
    def __init__(self, robot, window_width=1000,
                              window_height=750,
                              pixels_per_meter=100,
                              window_title="SCS3"):
        super().__init__(window_width, window_height, window_title)
        self.pixels_per_meter = pixels_per_meter
        self.world_origin_x = self.width / 2.0  # world origin x in window coordinates
        self.world_origin_y = self.height / 6.0 # world origin y in window coordinates
        self.objs_to_draw = []
    
    def world_to_window_coord_transform(self, x_world, y_world):
        '''Convert from world coordinates (x -> right, y -> up) to
            window coordinates (x -> right, y -> down)
        '''
        return (self.world_origin_x + x_world*self.pixels_per_meter, 
                self.world_origin_y + y_world*self.pixels_per_meter)

    def world_to_window_scale(self, x):
        return x*self.pixels_per_meter
    
    def add_obj_to_draw(self, obj_to_draw):
        self.objs_to_draw.append(obj_to_draw)
    
    def on_draw(self):
        self.clear()
        for obj_to_draw in self.objs_to_draw:
            obj_to_draw.draw(self.world_to_window_coord_transform,
                             self.world_to_window_scale)
    
    def start(self):
        pyglet.app.run() # blocks until window is closed