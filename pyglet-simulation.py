import pyglet
import numpy as np
import threading
import time


window_width = 1000
window_height = 750
window_title = "SCS3"

pixels_per_meter = 100

world_origin_x = window_width / 2.0          # World origin x in window coordinates
world_origin_y = window_height / 2.0         # World origin y in window coordinates

def world_to_window(x_world, y_world):
    '''Convert from world coordinates (x -> right, y -> up) to
        window coordinates (x -> right, y -> down)
    '''
    return (world_origin_x + x_world*pixels_per_meter, world_origin_y + y_world*pixels_per_meter)


class DefaultController():
    def __init__(self, nq, nv, nu):
        self.nq = nq
        self.nv = nv
        self.nu = nu
        
    def get_joint_control_inputs(self):
        return np.zeros(self.nu)
    
    
class LineArtist():
    def __init__(self, num_lines):
        self.num_lines = num_lines
        self.line_widths = [10]*self.num_lines
        self.line_colors = [(255, 255, 255)]*self.num_lines
        self.line_batch = pyglet.graphics.Batch()
        self.lines = [None] * self.num_lines
    
    def draw(self, points_in_line):
        assert len(points_in_line) > 1
        prev_point = points_in_line[0]
        for i, point in enumerate(points_in_line[1:]):
            prev_point_window = world_to_window(prev_point[0], prev_point[1])
            point_window = world_to_window(point[0], point[1])
            self.lines[i] = pyglet.shapes.Line(prev_point_window[0], prev_point_window[1],    # point 1 x, y
                                               point_window[0], point_window[1],              # point 2 x, y
                                               self.line_widths[i],
                                               self.line_colors[i],
                                               batch=self.line_batch) 
            prev_point = point
        self.line_batch.draw()

    
class DoublePendulum():
    def __init__(self):
        self.state = np.array([1, 0, 0, 0]) # theta 1, theta 2, theta 1 dot, theta 2 dot
        self.nq = 2
        self.nv = 2
        self.nu = self.nq
        self.m1 = 100.0
        self.m2 = 1.0
        self.l1 = 1.0
        self.l2 = 1.0
        self.g = 9.81
        
        self.p1 = None
        self.p2 = None
        
        self.artist = LineArtist(2)
        self.controller = DefaultController(self.nq, self.nv, self.nu)
    
    def dynamics(self, x, u):
        m1, m2, l1, l2 = self.m1, self.m2, self.l1, self.l2
        g = self.g
        t1, t2, t1dot, t2dot = x
        
        M = np.array([[(m1+m2)*l1**2 + m2*l2**2 + 2*m2*l1*l2*np.cos(t2),        m2*l2**2 + m2*l1*l2*np.cos(t2)],
                      [m2*l2**2 + m2*l1*l2*np.cos(t2),                          m2*l2**2]])
        C = np.array([[0,                           -m2*l1*l2*(2*t1dot + t2dot)*np.sin(t2)],
                      [m2*l1*l2*t1dot*np.sin(t2),   0]])
        tau = -np.array([(m1+m2)*g*l1*np.sin(t1) + m2*g*l2*np.sin(t1+t2),
                         m2*g*l2*np.sin(t1+t2)])
        
        qddot = np.linalg.inv(M) @ (tau + np.eye(2)@u - C@np.array([t1dot, t2dot]))
        xdot = np.array([t1dot, t2dot, qddot[0], qddot[1]])
        return xdot
    
    def draw(self):
        self.artist.draw(self.calculate_lines_start_end())
        
    def calculate_lines_start_end(self):
        t1, t2 = self.state[0], self.state[1]
        self.p1 = self.l1 * np.array([np.sin(t1),
                                      -np.cos(t1)])
        self.p2 = self.p1 + self.l2 * np.array([np.sin(t1 + t2),
                                                -np.cos(t1 + t2)])
        return np.array([np.zeros(2), self.p1, self.p2])


class RobotSimulation():
    def __init__(self, robot, dt=1e-3):
        self.robot = robot              # contains state and dynamics info
        self.dt = dt                    # in seconds
        self.run_simulation = True      # default to run simulation when run() is called
        self.simulation_thread = threading.Thread(target=self.run)
    
    def set_robot(self, robot):
        self.robot = robot
    
    def rk4(self, dynamics, x, u, dt):
        k1 = dt*dynamics(x, u)
        k2 = dt*dynamics(x+k1/2, u)
        k3 = dt*dynamics(x+k2/2, u)
        k4 = dt*dynamics(x+k3, u)
        return x + (k1 + 2*k2 + 2*k3 + k4)/6.0

    def simulate(self, u):
        self.robot.state = self.rk4(self.robot.dynamics, self.robot.state, u, self.dt)
    
    def run(self):
        start = time.perf_counter()
        while self.run_simulation:
            if time.perf_counter() - start >= self.dt:
                start = time.perf_counter()
                self.simulate(self.robot.controller.get_joint_control_inputs())
    
    def start_thread(self):
        self.simulation_thread.start()
    
    def stop_thread(self):
        self.run_simulation = False
    
    def draw(self):
        self.robot.draw()


window = pyglet.window.Window(window_width, window_height, window_title)

robot_simulation = RobotSimulation(DoublePendulum())

@window.event
def on_draw():
    window.clear()
    robot_simulation.draw()

robot_simulation.start_thread()
pyglet.app.run() # blocks until window is closed

robot_simulation.stop_thread()