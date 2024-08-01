import robots
import environments
import simulator

# robot = robots.DoublePendulum()
# robot = robots.SingleStick()
robot = robots.SingleBox()
environment = environments.DefaultEnvironment()
simulation = simulator.RobotSimulator(robot, environment)
simulation.start_threads()