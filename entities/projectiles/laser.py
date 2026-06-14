import pygame


class LaserProjectile:

    def __init__(self, start_pos, end_pos, target, damage, duration=6):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.target = target
        self.damage = damage
        self.duration = duration
        self.frames_left = duration
        self.active = True
        self.damage_applied = False

    def update(self):
        if not self.damage_applied:
            if self.target.alive:
                self.target.take_damage(self.damage)

            self.damage_applied = True

        self.frames_left -= 1

        if self.frames_left <= 0:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.line(
            overlay,
            (255, 40, 40, 179),
            self.start_pos,
            self.end_pos,
            4
        )
        screen.blit(overlay, (0, 0))
