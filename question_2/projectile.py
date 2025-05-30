import pygame

class Projectile:
    def __init__(self, x, y):
        # Create a small rectangle representing the projectile at (x, y)
        self.rect = pygame.Rect(x, y, 10, 5)  # Width: 10, Height: 5
        self.speed = 10                       # Projectile speed (pixels per frame)
        self.damage = 10                      # Damage dealt to enemies on collision

    def move(self):
        # Move the projectile to the right each frame
        self.rect.x += self.speed

    def draw(self, win):
        # Draw the projectile as a red rectangle on the game window
        pygame.draw.rect(win, (255, 0, 0), self.rect)
