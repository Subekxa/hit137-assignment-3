
import pygame

class Enemy:
    def __init__(self, x, y):
        # Create a rectangular hitbox for the enemy
        self.rect = pygame.Rect(x, y, 50, 60)
        self.speed = 2  # Speed at which the enemy moves
        self.health = 30  # Total health of the enemy
        self.direction = 1  # Movement direction: 1 for right, -1 for left

    def move(self):
        # Move the enemy in the current direction
        self.rect.x += self.speed * self.direction

        # Reverse direction if the enemy hits the edge of the screen
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.direction *= -1

    def draw(self, win):
        # Draw the enemy as a red rectangle on the screen
        pygame.draw.rect(win, (255, 0, 0), self.rect)

    def take_damage(self, amount):
        # Subtract damage from health
        self.health -= amount

    def is_alive(self):
        # Return True if enemy still has health
        return self.health > 0
