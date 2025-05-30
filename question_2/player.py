
import pygame
from projectile import Projectile

class Player:
    def __init__(self, x, y):
        # Initialize the player's rectangle (position and size)
        self.rect = pygame.Rect(x, y, 50, 60)  # Width: 50, Height: 60
        self.speed = 5                         # Horizontal movement speed
        self.jump_speed = -10                  # Negative value to move up
        self.gravity = 0.5                     # Gravity effect on vertical velocity
        self.velocity_y = 0                    # Current vertical velocity
        self.jumping = False                   # Flag to check if the player is in the air
        self.health = 100                      # Player's initial health
        self.lives = 3                         # Number of lives
        self.projectiles = []                  # List to hold projectiles shot by player

    def handle_movement(self, keys):
        # Handle horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Apply gravity to vertical velocity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Simulate ground collision (y=540)
        if self.rect.bottom >= 540:
            self.rect.bottom = 540
            self.jumping = False               # Player has landed
            self.velocity_y = 0                # Reset vertical velocity

    def jump(self):
        # Allow jumping only if not already in the air
        if not self.jumping:
            self.velocity_y = self.jump_speed  # Apply upward velocity
            self.jumping = True                # Set jumping flag

    def shoot(self):
        # Limit the number of active projectiles to 3
        if len(self.projectiles) < 3:
            proj = Projectile(self.rect.centerx, self.rect.y)  # Create new projectile
            self.projectiles.append(proj)                      # Add to projectile list

    def draw(self, win):
        # Draw the player as a blue rectangle
        pygame.draw.rect(win, (0, 0, 255), self.rect)

        # Draw all active projectiles
        for projectile in self.projectiles:
            projectile.draw(win)
