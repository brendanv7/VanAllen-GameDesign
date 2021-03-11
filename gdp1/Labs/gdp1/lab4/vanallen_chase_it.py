# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/
 
import pygame
import math

# Setup
pygame.init()

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

# Set the initial location and movement speed
x_coord = 10
y_coord = 10
X_SPEED = 3
Y_SPEED = 3

# Create the text
font = pygame.font.SysFont('Calibri', 25, True, False)
text = font.render("You're IT!", True, WHITE)

displayText = False

def draw_stick_figure(screen, x, y):
    # Head
    pygame.draw.ellipse(screen, WHITE, [1 + x, y, 10, 10], 0)
 
    # Legs
    pygame.draw.line(screen, WHITE, [5 + x, 17 + y], [10 + x, 27 + y], 2)
    pygame.draw.line(screen, WHITE, [5 + x, 17 + y], [x, 27 + y], 2)
 
    # Body
    pygame.draw.line(screen, GREEN, [5 + x, 17 + y], [5 + x, 7 + y], 2)
 
    # Arms
    pygame.draw.line(screen, BLUE, [5 + x, 7 + y], [9 + x, 17 + y], 2)
    pygame.draw.line(screen, BLUE, [5 + x, 7 + y], [1 + x, 17 + y], 2)

def update_coords():
    # Mouse coords
    pos = pygame.mouse.get_pos()
    x_mouse = pos[0]
    y_mouse = pos[1]

    # Calculate the angle to determine the movement of the stick
    global x_coord, y_coord, displayText
    x_distance = x_mouse - x_coord
    y_distance = y_mouse - y_coord

    theta = math.atan2(x_distance, y_distance)
    dx = X_SPEED * math.sin(theta)
    dy = Y_SPEED * math.cos(theta)

    # Update stick's coords
    x_coord += dx
    y_coord += dy

    # Determine if the stick caught the mouse
    x_caught = x_mouse - X_SPEED <= x_coord <= x_mouse + X_SPEED
    y_caught = y_mouse - Y_SPEED <= y_coord <= y_mouse + Y_SPEED

    if x_caught or y_caught:
        x_coord = x_mouse
        y_coord = y_mouse
        displayText = True
    else:
        displayText = False
  
# Set the width and height of the screen [width,height]
size = [700, 500]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(0)

# -------- Main Program Loop -----------
while not done:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Update
    update_coords()

    # Render
    screen.fill(BLACK)
    draw_stick_figure(screen, x_coord, y_coord)

    if displayText:
        screen.blit(text, [x_coord + 10, y_coord - 10])
     
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 20 frames per second
    clock.tick(60)
     
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
