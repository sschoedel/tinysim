import threading
import time
    
class RobotSimulator():
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