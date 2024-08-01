import visualizer
import environments

import threading
import time
    
class RobotSimulator():
    def __init__(self, robot, environment=None, dt=1e-4):
        self.robot = robot              # contains state and dynamics info
        if environment == None:
            self.environment = environments.DefaultEnvironment()
        else:
            self.environment = environment
        self.dt = dt                    # in seconds
        self.sim_thread = threading.Thread(target=self.run)
        self.run_simulation = True      # default to run simulation when run() is called
        self.vis = visualizer.RobotVisualizer(self.robot)
        # add anything we want to be drawn to visualizer
        self.vis.add_obj_to_draw(self.robot)
        self.vis.add_obj_to_draw(self.environment)
    
    def rk4(self, dynamics, x, u, dt):
        k1 = dt*dynamics(x, u)
        k2 = dt*dynamics(x+k1/2, u)
        k3 = dt*dynamics(x+k2/2, u)
        k4 = dt*dynamics(x+k3, u)
        return x + (k1 + 2*k2 + 2*k3 + k4)/6.0

    def simulate(self, u):
        # detect collision points
        
        # compute forces
        
        # simulate
        self.robot.state = self.rk4(self.robot.dynamics, self.robot.state, u, self.dt)
    
    def run(self):
        start = time.perf_counter()
        while self.run_simulation:
            if time.perf_counter() - start >= self.dt:
                start = time.perf_counter()
                self.simulate(self.robot.controller.get_joint_control_inputs())
    
    def start_threads(self):
        self.sim_thread.start() # starts simulation thread
        self.vis.start() # starts pygame thread (blocking)
        self.run_simulation = False # stops simulation thread once pygame thread finishes