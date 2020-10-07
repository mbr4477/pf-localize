from .world import Line
import pygame
import numpy as np
pygame.init()

class RobotSprite(pygame.sprite.Sprite):
    def __init__(self, containers):
        pygame.sprite.Sprite.__init__(self, containers)
        self.orig_image = pygame.Surface((20, 10), pygame.SRCALPHA)
        self.orig_image.fill((0,100,255))
        self.image = pygame.transform.rotate(self.orig_image, 0)
        self.rect = self.image.get_rect()
        self.angle = 0

    def update(self):
        self.image = pygame.transform.rotate(self.orig_image, -self.angle/np.pi*180.0)
        self.rect = self.image.get_rect(center=self.rect.center)

class ParticleSprite(pygame.sprite.Sprite):
    def __init__(self, containers):
        pygame.sprite.Sprite.__init__(self, containers)
        self.image = pygame.Surface((2,2))
        self.image.fill((200,200,200))
        self.rect = self.image.get_rect()

class Renderer:
    def __init__(self, width, height, num_particles, camera=(0,0), scale=1.0):
        self.width = width
        self.height = height
        self.camera = camera
        self.scale = scale
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((width, height))
        self.all = pygame.sprite.RenderUpdates()
        self.robot_sprite = RobotSprite(self.all) 
        self.background = pygame.Surface((width, height))
        self.background.fill((255,255,255))
        self.particle_sprites = []
        for p in range(num_particles):
            self.particle_sprites.append(ParticleSprite(self.all))

    def to_camera(self, pos):
        return (
            self.width//2 + (pos[0] - self.camera[0])*self.scale,
            self.height//2 + (pos[1] - self.camera[1])*self.scale
        )

    def clear(self):
        self.display.fill((255,255,255))

    def set_world(self, world):
        self.background.fill((255,255,255))
        for obs in world.obstacles:
            if isinstance(obs, Line):
                start = self.to_camera(obs.start)
                end = self.to_camera(obs.end)
                pygame.draw.line(self.background, (0,0,0), start, end, 5)
        self.display.blit(self.background, (0,0))
        pygame.display.flip()

    def render_robot(self, robot):
        pos = self.to_camera((robot.x, robot.y))
        self.robot_sprite.rect.center = pos
        self.robot_sprite.angle = robot.angle

    def render_particles(self, particles):
        for p,sprite in zip(particles, self.particle_sprites):
            sprite.rect.center = self.to_camera(tuple(p))

    def handle_frame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.all.clear  (self.display, self.background)
        self.all.update()
        dirty = self.all.draw(self.display)
        pygame.display.update(dirty)
        self.clock.tick(60)