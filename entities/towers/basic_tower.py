from entities.towers.tower import Tower
from systems.tags import MASS_PRODUCED
from systems.tags import ARMORED

class BasicTower(Tower):
    cannon_sprite_file = "Gatling_Turret_Laser.png"
    projectile_type = "laser"
    tags = [MASS_PRODUCED]
    tag_damage_modifiers = {
        MASS_PRODUCED: 5,
        ARMORED: -5
    }
    cost = 50
    damage = 25
    range_radius = 180
    fire_rate = 45
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
