import pygame
import sys
from player import Player
from projectile import Projectile
from enemy import Enemy
from boss import Boss
from collectible import Collectible
from levels import get_level
from game_over import game_over_screen

# Initialize Pygame
pygame.init()

# Set window dimensions and create display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Hero Side Scroller")

# Set FPS and clock
clock = pygame.time.Clock()
FPS = 60

# Set font for UI text
font = pygame.font.SysFont("comicsans", 30)

# Helper function to draw health bars
def draw_health_bar(win, x, y, health, max_health, width=100, height=10):
    ratio = health / max_health
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))  # Background (red)
    pygame.draw.rect(win, (0, 255, 0), (x, y, width * ratio, height))  # Health (green)

# Main game loop
def main():
    player = Player(100, 480)  # Create the player object
    score = 0
    level = 1
    enemies, collectibles, boss = get_level(level)  # Load first level
    game_over = False
    won = False

    while True:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_f:
                    player.shoot()
                if game_over and event.key == pygame.K_r:
                    main()  # Restart game
                if game_over and event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            # Handle player movement
            player.handle_movement(keys)

            # Handle projectiles
            for projectile in player.projectiles[:]:
                projectile.move()
                if projectile.rect.x > WIDTH:
                    player.projectiles.remove(projectile)

            # Enemy interaction
            for enemy in enemies[:]:
                enemy.move()
                for projectile in player.projectiles[:]:
                    if enemy.rect.colliderect(projectile.rect):
                        enemy.take_damage(projectile.damage)
                        player.projectiles.remove(projectile)
                        if not enemy.is_alive():
                            enemies.remove(enemy)
                            score += 10

            # Boss interaction (Level 3)
            if boss:
                boss.move()
                for projectile in player.projectiles[:]:
                    if boss.rect.colliderect(projectile.rect):
                        boss.take_damage(projectile.damage)
                        player.projectiles.remove(projectile)
                        if not boss.is_alive():
                            boss = None
                            score += 50
                            won = True
                            game_over = True

            # Player collision with enemies
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    player.health -= 1
                    if player.health <= 0:
                        player.lives -= 1
                        player.health = 100
                        if player.lives <= 0:
                            game_over = True

            # Player collision with boss
            if boss and player.rect.colliderect(boss.rect):
                player.health -= 2
                if player.health <= 0:
                    player.lives -= 1
                    player.health = 100
                    if player.lives <= 0:
                        game_over = True

            # Player collision with collectibles
            for collectible in collectibles[:]:
                if player.rect.colliderect(collectible.rect):
                    if collectible.type == "health":
                        player.health = min(player.health + 30, 100)
                        score += 5
                    elif collectible.type == "life":
                        player.lives += 1
                        score += 10
                    collectibles.remove(collectible)

            # Advance to next level
            if not enemies and not boss:
                level += 1
                if level > 3:
                    won = True
                    game_over = True
                else:
                    enemies, collectibles, boss = get_level(level)
                    player.rect.x = 100  # Reset player position

        # Draw background
        win.fill((135, 206, 235))  # Sky blue

        # Draw ground
        pygame.draw.rect(win, (50, 205, 50), (0, 540, WIDTH, 60))

        # Draw all game elements
        player.draw(win)
        for enemy in enemies:
            enemy.draw(win)
        if boss:
            boss.draw(win)
        for collectible in collectibles:
            collectible.draw(win)

        # UI: Health, Lives, Score, Level
        draw_health_bar(win, 10, 10, player.health, 100)
        lives_text = font.render(f"Lives: {player.lives}", True, (0, 0, 0))
        win.blit(lives_text, (10, 30))

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        win.blit(score_text, (650, 10))
        level_text = font.render(f"Level: {level}", True, (0, 0, 0))
        win.blit(level_text, (650, 30))

        # Game over screen
        if game_over:
            game_over_screen(win, score, won)

        pygame.display.update()

# Start the game
if __name__ == "__main__":
    main()
