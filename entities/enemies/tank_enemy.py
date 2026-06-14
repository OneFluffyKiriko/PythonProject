from entities.enemies.enemy import Enemy
from systems.tags import ARMORED

class TankEnemy(Enemy):
    tags = [ARMORED]
    health = 500
    speed = 1
    metal_reward = 50
    sprite_file = "Armored_Robot.png"
    info = ""

    def __init__(self, path):
        super().__init__(
            path,
            health=self.health,
            speed=self.speed,
            metal_reward=self.metal_reward,
            sprite_file=self.sprite_file
        )
