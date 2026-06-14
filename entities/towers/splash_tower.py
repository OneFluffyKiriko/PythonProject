from entities.towers.tower import Tower
from systems.tags import ARMORED


class SplashTower(Tower):
    cannon_sprite_file = "Cannon_Turret_Launcher.png"
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
