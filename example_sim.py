import robots
import simulator
import visualizer

# robot = robots.DoublePendulum()
robot = robots.SingleStick()
robot_simulation = simulator.RobotSimulator(robot)
robot_visualizer = visualizer.RobotVisualizer(robot)

robot_simulation.start_thread()
robot_visualizer.start()

robot_simulation.stop_thread()