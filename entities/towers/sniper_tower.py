from entities.towers.tower import Tower
from systems.tags import HIGH_TECH
from systems.tags import ARMORED

class SniperTower(Tower):
    cannon_sprite_file = "Sniper_Turret_Laser.png"
    projectile_type = "laser"
    tags = [HIGH_TECH]
    tag_damage_modifiers = {
        HIGH_TECH: 20,
        ARMORED: -10
    }
    cost = 120
    damage = 80
    range_radius = 350
    fire_rate = 120
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
