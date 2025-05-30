

import pygame

class Boss:
    def __init__(self, x, y):
        # Create a larger rectangle for the boss enemy
        self.rect = pygame.Rect(x, y, 100, 120)
        self.speed = 3               # Boss movement speed
        self.health = 150            # Higher health than normal enemies
        self.direction = 1           # 1 = right, -1 = left (initial direction)

    def move(self):
        # Move boss horizontally
        self.rect.x += self.speed * self.direction
        # Change direction when boss hits screen boundaries
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.direction *= -1

    def draw(self, win):
        # Draw the boss as a purple rectangle
        pygame.draw.rect(win, (128, 0, 128), self.rect)

    def take_damage(self, amount):
        # Reduce boss health when hit by a projectile
        self.health -= amount

    def is_alive(self):
        # Return True if boss is still alive
        return self.health > 0
