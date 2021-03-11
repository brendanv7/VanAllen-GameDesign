"""
 Show how to use a sprite backed by a graphic.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""

import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
ORANGE   = ( 255, 165,   0)
BLUE     = (   0,   0, 255)

pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Brendan's Palace")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

    # --- Game logic should go here

    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    # Main part
    pygame.draw.rect(screen, ORANGE, [250, 150, 200, 200], 0)

    # Chimney
    pygame.draw.rect(screen, BLACK, [260, 110, 20, 30], 0)

    # White filled roof to cover part of the chimney
    pygame.draw.polygon(screen, WHITE, [[350, 50], [250, 150], [450, 150]], 0)

    # Roof - this is the actual outline
    pygame.draw.polygon(screen, ORANGE, [[350, 50], [250, 150], [450, 150]], 5)

    # Windows
    window_x_coord = 280
    window_y_coord = 200
    for i in range(4):
        pygame.draw.rect(screen, BLUE, [window_x_coord, window_y_coord, 10, 30], 0)
        window_x_coord += 45

    # Door
    pygame.draw.rect(screen, GREEN, [340, 300, 20, 50], 0)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

