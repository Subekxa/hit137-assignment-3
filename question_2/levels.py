from enemy import Enemy
from boss import Boss
from collectible import Collectible

# This function sets up the enemies, collectibles, and boss for each level
def get_level(level_num):
    if level_num == 1:
        # Level 1: Two enemies, one health collectible
        enemies = [Enemy(400, 480), Enemy(600, 480)]
        collectibles = [Collectible(200, 510, "health")]
        boss = None  # No boss in level 1

    elif level_num == 2:
        # Level 2: Three enemies, one health and one life collectible
        enemies = [Enemy(300, 480), Enemy(500, 480), Enemy(700, 480)]
        collectibles = [
            Collectible(150, 510, "health"),
            Collectible(650, 510, "life")
        ]
        boss = None  # No boss in level 2

    elif level_num == 3:
        # Level 3: Three enemies, one health and one life collectible, final boss appears
        enemies = [Enemy(250, 480), Enemy(450, 480), Enemy(650, 480)]
        collectibles = [
            Collectible(350, 510, "health"),
            Collectible(550, 510, "life")
        ]
        boss = Boss(600, 420)  # Boss appears in the final level

    else:
        # If level number is greater than 3, return empty lists
        enemies = []
        collectibles = []
        boss = None

    return enemies, collectibles, boss
