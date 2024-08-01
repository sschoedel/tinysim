import numpy as np

import visualizer
import controllers
    
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
        
        self.artist = visualizer.LineArtist(2)
        self.controller = controllers.DefaultController(self.nq, self.nv, self.nu)
    
    def dynamics(self, x, u):
        assert len(x) == len(self.state)
        assert len(u) == self.nu
        
        m1, m2, l1, l2 = self.m1, self.m2, self.l1, self.l2
        g = self.g
        t1, t2, t1dot, t2dot = x
        
        M = np.array([[(m1+m2)*l1**2 + m2*l2**2 + 2*m2*l1*l2*np.cos(t2),        m2*l2**2 + m2*l1*l2*np.cos(t2)],
                      [m2*l2**2 + m2*l1*l2*np.cos(t2),                          m2*l2**2]])
        C = np.array([[0,                           -m2*l1*l2*(2*t1dot + t2dot)*np.sin(t2)],
                      [m2*l1*l2*t1dot*np.sin(t2),   0]])
        tau = -np.array([(m1+m2)*g*l1*np.sin(t1) + m2*g*l2*np.sin(t1+t2),
                         m2*g*l2*np.sin(t1+t2)])
        
        qddot = np.linalg.inv(M) @ (tau + np.eye(self.nu)@u - C@np.array([t1dot, t2dot]))
        xdot = np.array([t1dot, t2dot, *qddot])
        return xdot
    
    def calculate_lines_start_end(self):
        t1, t2 = self.state[0], self.state[1]
        self.p1 = self.l1 * np.array([np.sin(t1),
                                      -np.cos(t1)])
        self.p2 = self.p1 + self.l2 * np.array([np.sin(t1 + t2),
                                                -np.cos(t1 + t2)])
        return np.array([np.zeros(2), self.p1, self.p2])
    
    def draw(self, world_to_window_coord_transform, world_to_window_scale):
        self.artist.draw(self.calculate_lines_start_end(),
                         world_to_window_coord_transform,
                         world_to_window_scale)


class SingleStick():
    def __init__(self):
        # self.state = np.array([0, 0, 0, 1, 5, 3]) # x, y, theta, x dot, y dot, theta dot
        self.state = np.array([0, 3, np.pi/2, 0, 0, 0]) # x, y, theta, x dot, y dot, theta dot
        self.nq = 3
        self.nv = 3
        self.nu = self.nq
        self.m = 1.0
        self.I = 1.0
        self.length = 1.0
        self.g = 9.81
        
        self.p1 = None
        self.p2 = None
        
        self.artist = visualizer.LineArtist(1)
        self.controller = controllers.DefaultController(self.nq, self.nv, self.nu)

    def dynamics(self, x, u):
        assert len(x) == len(self.state)
        assert len(u) == self.nu
        
        m, I, g = self.m, self.I, self.g
        xdot, ydot, thetadot = x[3:]
        
        M = np.array([[m, 0, 0],
                      [0, m, 0],
                      [0, 0, I]])
        C = np.zeros((3,3))
        tau = -np.array([0,
                         m*g,
                         0])
        
        qddot = np.linalg.inv(M) @ (tau + np.eye(self.nu)@u - C@np.array([xdot, ydot, thetadot]))
        return np.array([xdot, ydot, thetadot, *qddot])
    
    def calculate_lines_start_end(self):
        x, y, theta = self.state[0], self.state[1], self.state[2]
        self.p1 = np.array([x, y]) + self.length * np.array([np.sin(theta), -np.cos(theta)]) / 2.0
        self.p2 = np.array([x, y]) - self.length * np.array([np.sin(theta), -np.cos(theta)]) / 2.0
        return np.array([self.p1, self.p2])
    
    def draw(self, world_to_window_coord_transform, world_to_window_scale):
        self.artist.draw(self.calculate_lines_start_end(),
                         world_to_window_coord_transform,
                         world_to_window_scale)


class SingleBox():
    def __init__(self):
        self.state = np.array([0, 3, 0, 0, 0, 0]) # x, y, theta, x dot, y dot, theta dot
        self.nq = 3
        self.nv = 3
        self.nu = self.nq
        self.m = 1.0
        self.I = 1.0
        self.width = 1.0
        self.g = 9.81
        
        self.p1 = None
        self.p2 = None
        
        self.artist = visualizer.RectangleArtist(self.width)
        self.controller = controllers.DefaultController(self.nq, self.nv, self.nu)

    def dynamics(self, x, u):
        assert len(x) == len(self.state)
        assert len(u) == self.nu
        
        m, I, g = self.m, self.I, self.g
        xdot, ydot, thetadot = x[3:]
        
        M = np.array([[m, 0, 0],
                      [0, m, 0],
                      [0, 0, I]])
        C = np.zeros((3,3))
        tau = -np.array([0,
                         m*g,
                         0])
        
        qddot = np.linalg.inv(M) @ (tau + np.eye(self.nu)@u - C@np.array([xdot, ydot, thetadot]))
        return np.array([xdot, ydot, thetadot, *qddot])
    
    def draw(self, world_to_window_coord_transform, world_to_window_scale):
        self.artist.draw(self.state[0], self.state[1],
                         self.width, self.width,
                         self.state[2],
                         world_to_window_coord_transform,
                         world_to_window_scale)
