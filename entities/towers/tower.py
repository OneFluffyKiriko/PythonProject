import math
from pathlib import Path

import pygame

from entities.projectiles.laser import LaserProjectile
from entities.projectiles.projectile import Projectile
from systems.tags import get_matching_tags


ASSET_DIR = Path(__file__).resolve().parents[2] / "assets"


class Tower:
    loaded_sprites = {}
    base_sprite_file = "Turret_Base.png"
    cannon_sprite_file = None
    sprite_scale = 1.0
    sprite_angle_offset = 0
    tags = []
    tag_damage_modifiers = {}
    projectile_type = "projectile"

    def __init__(
        self,
        grid_x,
        grid_y,
        damage,
        range_radius,
        fire_rate,
        cost
    ):
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.x = grid_x
        self.y = grid_y

        self.damage = damage
        self.range = range_radius

        self.fire_rate = fire_rate
        self.cost = cost
        self.tags = list(self.tags)
        self.tag_damage_modifiers = dict(self.tag_damage_modifiers)

        self.cooldown = 0
        self.angle = 0
        self.base_sprite = self.load_sprite(self.base_sprite_file)
        self.cannon_sprite = self.load_sprite(self.cannon_sprite_file)

    @classmethod
    def load_sprite(cls, sprite_file):
        if sprite_file is None:
            return None

        if sprite_file not in cls.loaded_sprites:
            image = pygame.image.load(ASSET_DIR / sprite_file).convert_alpha()
            cls.loaded_sprites[sprite_file] = image

        return cls.loaded_sprites[sprite_file]

    def get_target(self, enemies):

        closest = None
        closest_distance = float("inf")

        for enemy in enemies:

            if not enemy.alive:
                continue

            distance = math.hypot(
                enemy.x - self.x,
                enemy.y - self.y
            )

            if distance <= self.range:

                if distance < closest_distance:
                    closest_distance = distance
                    closest = enemy

        return closest

    def update(self, enemies, projectiles):

        if self.cooldown > 0:
            self.cooldown -= 1

        target = self.get_target(enemies)

        if target:
            self.angle = -math.degrees(
                math.atan2(target.y - self.y, target.x - self.x)
            ) - 90

        if target and self.cooldown <= 0:

            projectiles.append(
                self.create_projectile(target)
            )

            self.cooldown = self.fire_rate

    def create_projectile(self, target):
        if self.projectile_type == "laser":
            return LaserProjectile(
                self.get_projectile_start_point(target),
                self.get_projectile_end_point(target),
                target,
                self.get_damage_against(target)
            )

        return Projectile(
            self.x,
            self.y,
            target,
            self.get_damage_against(target),
            8
        )

    def get_projectile_start_point(self, target):
        return (int(self.x), int(self.y))

    def get_projectile_end_point(self, target):
        return (int(target.x), int(target.y))

    def get_damage_against(self, enemy):
        bonus_damage = sum(
            self.tag_damage_modifiers.get(tag, 0)
            for tag in get_matching_tags(
                self.tags,
                getattr(enemy, "tags", [])
            )
        )

        return self.damage + bonus_damage

    def draw(self, screen):
        if self.base_sprite:
            base = self._scaled_sprite(self.base_sprite)
            base_rect = base.get_rect(
                center=(int(self.x), int(self.y))
            )
            screen.blit(base, base_rect)

        if self.cannon_sprite:
            cannon = self._scaled_sprite(self.cannon_sprite)
            rotated_cannon = pygame.transform.rotate(
                cannon,
                self.angle + self.sprite_angle_offset
            )
            cannon_rect = rotated_cannon.get_rect(
                center=(int(self.x), int(self.y))
            )
            screen.blit(rotated_cannon, cannon_rect)

    def _scaled_sprite(self, sprite):
        if self.sprite_scale == 1.0:
            return sprite

        width, height = sprite.get_size()
        return pygame.transform.smoothscale(
            sprite,
            (
                max(1, int(width * self.sprite_scale)),
                max(1, int(height * self.sprite_scale))
            )
        )
