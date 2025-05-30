import pygame

# Function to display the game over or victory screen
def game_over_screen(win, score, won=False):
    # Fill the window with black background
    win.fill((0, 0, 0))

    # Use a large font for the main message
    font = pygame.font.SysFont("comicsans", 50)

    # Display a win or lose message based on the game result
    if won:
        text = font.render("You Win! Score: " + str(score), True, (0, 255, 0))  # Green for win
    else:
        text = font.render("Game Over! Score: " + str(score), True, (255, 0, 0))  # Red for lose

    # Display the message at the center of the screen
    win.blit(text, (100, 250))

    # Use a smaller font for instructions
    font2 = pygame.font.SysFont("comicsans", 30)
    restart_text = font2.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    
    # Display the restart/quit instruction
    win.blit(restart_text, (150, 320))

    # Update the screen with changes
    pygame.display.update()
