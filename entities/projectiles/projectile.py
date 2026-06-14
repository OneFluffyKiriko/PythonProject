import pygame
import math

class Projectile:

    def __init__(self, x, y, target, damage, speed):
        self.x = x
        self.y = y

        self.target = target

        self.damage = damage
        self.speed = speed

        self.active = True

    def update(self):
        if not self.target.alive:
            self.active = False
            return

        dx = self.target.x - self.x
        dy = self.target.y - self.y

        distance = math.hypot(dx, dy)

        if distance < self.speed:
            self.target.take_damage(self.damage)
            self.active = False
            return

        self.x += dx / distance * self.speed
        self.y += dy / distance * self.speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 255, 0),
            (int(self.x), int(self.y)),
            4
        )