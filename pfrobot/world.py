import numpy as np
import shapely.geometry

class Obstacle:
  def intersection(self, x1, y1, x2, y2):
    raise NotImplementedError()

class Line(Obstacle):
  def __init__(self, x1, y1, x2, y2):
    self.start = (x1, y1)
    self.end = (x2, y2)

  def intersection(self, x1, y1, x2, y2):
    other = shapely.geometry.LineString([(x1, y1), (x2, y2)])
    me = shapely.geometry.LineString([self.start, self.end])
    if not other.intersects(me):
      return np.array((np.inf, np.inf))
    return np.array(list(other.intersection(me).coords)[0])

# class Block(Obstacle):
#   def __init__(self, x, y, width, height):
#     self.x = x
#     self.y = y
#     self.width = width
#     self.height = height

#   def intersection(self, x1, y1, x2, y2):
#     line = shapely.geometry.LineString([(x1, y1), (x2, y2)])
#     rect = shapely.geometry.Polygon([
#       (self.x,self.y),
#       (self.x+self.width,self.y),
#       (self.x+self.width,self.y+self.height),
#       (self.x,self.y+self.height)
#     ])
#     if not line.intersects(rect):
#       return np.array((np.inf, np.inf))

#     int_points = line.intersection(rect)
#     closest_dist = np.inf
#     closest_point = (np.inf, np.inf)
#     for point in list(int_points.coords):
#       dist = (point[0] - x1)**2 + (point[1] - y1)**2
#       if dist < closest_dist:
#         closest_dist = dist
#         closest_point = point
#     return np.array(closest_point)
    
class World:
  def __init__(self):
    self.obstacles = []

  def add_obstacle(self, obs):
    self.obstacles.append(obs)

  def get_robot_sensor_values(self, robot):
    values = []
    for sensor in robot.sensors:
      angle = robot.angle + sensor.mount_angle
      end_x = sensor.range * np.cos(angle) + robot.x
      end_y = sensor.range * np.sin(angle) + robot.y
      min_dist = np.inf
      for obs in self.obstacles:
        point = obs.intersection(robot.x, robot.y, end_x, end_y)
        if point[0] != np.inf:
          dist = np.sqrt((point[0] - robot.x)**2 + (point[1] - robot.y)**2)
          if dist <= min_dist:
            min_dist = dist
      values.append(min_dist)
    return np.array(values)
    