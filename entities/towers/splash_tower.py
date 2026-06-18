from entities.towers.tower import Tower
from systems.tags import ARMORED


class SplashTower(Tower):
    cannon_sprite_file = "Cannon_Turret_Launcher.png"
    fire_sound = "cannon_turret"
    projectile_forward_offset = 22
    barrel_side_offset = 6
    tags = [ARMORED]
    tag_damage_modifiers = {
        ARMORED: 25
    }
    cost = 90
    damage = 40
    range_radius = 150
    fire_rate = 60
    info = ""

    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            damage=self.damage,
            range_radius=self.range_radius,
            fire_rate=self.fire_rate,
            cost=self.cost
        )
        self.next_barrel_side = -1

    def get_projectile_start_point(self, target):
        side_offset = self.barrel_side_offset * self.next_barrel_side
        self.next_barrel_side *= -1

        return self.get_offset_projectile_start_point(
            target,
            self.projectile_forward_offset,
            side_offset
        )
