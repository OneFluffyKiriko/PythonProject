from entities.towers.tower import Tower
from systems.tags import MASS_PRODUCED
from systems.tags import ARMORED

class BasicTower(Tower):
    cannon_sprite_file = "Gatling_Turret_Laser.png"
    projectile_type = "laser"
    fire_sound = "laser_turret"
    projectile_forward_offset = 22
    barrel_side_offset = 5
    tags = [MASS_PRODUCED]
    tag_damage_modifiers = {
        MASS_PRODUCED: 15,
        ARMORED: -5
    }
    cost = 60
    damage = 15
    range_radius = 200
    fire_rate = 35
    info = "The SynTech Gatling Laser Mk3, this model comes with alternating barrels for even more cooling, and even more firepower."

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
