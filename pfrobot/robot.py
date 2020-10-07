import numpy as np
import time
import pygame

class Sensor:
  def __init__(self, mount_angle, range):
    self.mount_angle = mount_angle
    self.range = range

class Robot:
  def __init__(self, x, y, angle, sensors=[]):
    self.x = x
    self.y = y
    self.angle = angle
    self.sensors = sensors

  def update(self, speed, dtheta, delta_time):
    self.angle += dtheta*delta_time
    self.x += np.cos(self.angle)*speed*delta_time
    self.y += np.sin(self.angle)*speed*delta_time

class RobotController:
  def update(self, sensor_values):
    keys = pygame.key.get_pressed()
    dtheta = 0
    speed = 0
    if keys[pygame.K_w]:
      speed = 15
    if keys[pygame.K_d]:
      dtheta = 2
    elif keys[pygame.K_a]:
      dtheta = -2
        
    return speed, dtheta

