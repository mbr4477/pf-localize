from .robot import Robot, Sensor, RobotController
from .world import World, Line
from .filtering import ParticleFilter
from .renderer import Renderer
import numpy as np
import time

# create the robot
robot = Robot(25, 25, 0)
robot.sensors.append(Sensor(0, 100))
robot.sensors.append(Sensor(np.pi/2, 100))
robot.sensors.append(Sensor(-np.pi/2, 100))
robot.sensors.append(Sensor(np.pi, 100))

# create the controller
controller = RobotController()

# create the world
world = World()
world.add_obstacle(Line(0,0,0,100))
world.add_obstacle(Line(0,0,100,0))
world.add_obstacle(Line(100,0,100,100))
world.add_obstacle(Line(0,100,100,100))
world.add_obstacle(Line(50,0,50,50))
world.add_obstacle(Line(0,50,20,50))

renderer = Renderer(num_particles=200, width=640, height=480, camera=(50,50), scale=3.0)

last_time = time.time()
renderer.set_world(world)

def meas_func(particles):
    fake_robot = Robot(0,0,robot.angle, robot.sensors)
    measurements = []
    for i in range(particles.shape[0]):
        fake_robot.x = particles[i,0]
        fake_robot.y = particles[i,1]
        measurements.append(world.get_robot_sensor_values(fake_robot))
    return np.array(measurements)

# particle filter
pf = ParticleFilter(
    state_func=lambda x: x, 
    state_noise_var=1.0, 
    meas_func=meas_func, 
    meas_noise_var=5.0, 
    num_particles=100, 
    shape=(2,)
)
pf.init_prior_particles((0,100), (0,100))

while True:
    now = time.time()
    sensor_values = world.get_robot_sensor_values(robot)
    speed, dtheta = controller.update(sensor_values=sensor_values)
    delta_time = now - last_time
    robot.update(speed, dtheta, delta_time)
    pf.state_tran_func = lambda p: p + np.array((np.cos(robot.angle)*speed*delta_time, np.sin(robot.angle)*speed*delta_time))
    pf.update(sensor_values)
    last_time = now

    # renderer.clear()
    renderer.render_robot(robot)
    renderer.render_particles(pf.particles)
    renderer.handle_frame()