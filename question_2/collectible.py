
import pygame

class Collectible:
    def __init__(self, x, y, type):
        # Create a rectangular area for the collectible
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = type  # Type of collectible: "health" or "life"

    def draw(self, win):
        # Set color based on the type of collectible
        if self.type == "health":
            color = (0, 255, 0)  # Green for health boost
        elif self.type == "life":
            color = (255, 255, 0)  # Yellow for extra life
        else:
            color = (255, 255, 255)  # Default color for unknown type

        # Draw the collectible on the game window
        pygame.draw.rect(win, color, self.rect)
