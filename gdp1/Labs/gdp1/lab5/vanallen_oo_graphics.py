"""
 A simple demonstration of object-oriented programming
 in Python using objects.

 Author: Brendan Van Allen
"""

import pygame
import random


class Rectangle:
    def __init__(self):
        # X location randomized between 0-700 (inclusive)
        self.x = random.randrange(0, 701)

        # Y location randomized between 0-500 (inclusive)
        self.y = random.randrange(0, 501)

        # Width and height randomized between 20-70 (inclusive)
        self.width = random.randrange(20, 71)
        self.height = random.randrange(20, 71)

        # Changes in x and y randomized between (-3)-3 (inclusive)
        self.change_x = random.randrange(-3, 4)
        self.change_y = random.randrange(-3, 4)

        # Color has randomized values between 0-255 (inclusive) for R, G, and B
        rand_R = random.randrange(0, 256)
        rand_G = random.randrange(0, 256)
        rand_B = random.randrange(0, 256)
        self.color = (rand_R, rand_G, rand_B)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])

    def move(self):
        self.x += self.change_x
        self.y += self.change_y


class Ellipse(Rectangle):
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, [self.x, self.y, self.width, self.height])

pygame.init()

pygame.display.set_caption("Brendan's Kaleidoscope")
size = (700, 500)
screen = pygame.display.set_mode(size)

# Flag to indicate if user has quit the game
done = False

clock = pygame.time.Clock()

BLACK = (0, 0, 0)

# Create the shapes
my_list = []

# Add 10 rectangles
for i in range(5000):
    my_object = Rectangle()
    my_list.append(my_object)

# Add 10 ellipses
for i in range(5000):
    my_object = Ellipse()
    my_list.append(my_object)


# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Update
    for shape in my_list:
        shape.move()

    # --- Render
    screen.fill(BLACK)

    for shape in my_list:
        shape.draw(screen)

    # Flip the buffers
    pygame.display.flip()

    # 60 fps
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

