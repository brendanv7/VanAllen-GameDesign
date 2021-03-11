import pygame


# This class handles sprite sheets. This was taken from:
# www.scriptefun.com/transcript-2-usingsprite-sheets-and-drawing-the-background
class Spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.convert_alpha(image)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip_horizontal(self, rect, image_count, colorkey=None):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_strip_vertical(self, rect, image_count, colorkey=None):
        tups = [(rect[0], rect[1]+rect(3)*y, rect[2], rect[3])
                for y in range(image_count)]
        return self.images_at(tups, colorkey)
