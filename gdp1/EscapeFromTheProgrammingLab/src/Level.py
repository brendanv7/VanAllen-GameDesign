import pygame
import constants
from GameObject import GameObject, Openable, TV, Door, Cabinet, Safe, \
    KeycardSafe, Item, Keycard, Poster
from Player import Player, HitBox


# Contains information for each level.
# Should be subclassed by each actual level
class Level(object):
    OFFSCREEN_POS = [-100, -100]

    NO_SIZE = [100, 100]

    def __init__(self, background):

        # Sprite lists
        self.all_sprites_list = pygame.sprite.Group()
        self.object_list = pygame.sprite.Group()
        self.interactable_list = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites_list.add(self.player)
        self.all_sprites_list.add(self.player.inventory)

        self.background = background

        # Loads the background image if there is one
        if isinstance(self.background, tuple):
            self.image = None
        else:
            self.image = pygame.image.load(self.background)

        self.complete = False

    def update(self):
        self.all_sprites_list.update()

    def draw(self, screen):
        # Draws background color or image
        if self.image is None:
            screen.fill(self.background)
        else:
            screen.blit(self.image, [0, 0])

        self.all_sprites_list.draw(screen)


class SplashScreen(Level):
    TEXT_X = constants.SCREEN_WIDTH // 2
    TEXT_Y = (constants.SCREEN_HEIGHT // 2) - 100
    TEXT_OFFSET_Y = 80

    def __init__(self):
        super().__init__(constants.WHITE)
        self.background = pygame.image.load("images/background.jpg")
        self.background = pygame.transform.scale(self.background,
                                                 (constants.SCREEN_WIDTH,
                                                  constants.SCREEN_HEIGHT))
        self.rect = self.background.get_rect()

        # Font is initalized here due to a bug where an error occurs in the
        # draw method if the font is not initalized
        pygame.font.init()

    def draw(self, screen):
        # Background image
        screen.fill(constants.WHITE)
        screen.blit(self.background, self.rect)

        # Game title
        font = pygame.font.SysFont("serif", 80)
        text = font.render("Escape the Programming Lab", True, constants.WHITE)
        text_x = SplashScreen.TEXT_X - (text.get_width() // 2)
        text_y = SplashScreen.TEXT_Y - (text.get_height() // 2)
        screen.blit(text, [text_x, text_y])

        # Author
        font = pygame.font.SysFont("serif", 50)
        text = font.render("Created by Brendan Van Allen", True,
                           constants.WHITE)
        text_x = SplashScreen.TEXT_X - (text.get_width() // 2)
        text_y = (SplashScreen.TEXT_Y - (
                text.get_height() // 2)) + SplashScreen.TEXT_OFFSET_Y
        screen.blit(text, [text_x, text_y])

        # Version
        font = pygame.font.SysFont("serif", 30)
        text = font.render("Version: beta (0.3)", True, constants.WHITE)
        text_x = SplashScreen.TEXT_X - (text.get_width() // 2)
        text_y = (SplashScreen.TEXT_Y - (text.get_height() // 2)) + (
                SplashScreen.TEXT_OFFSET_Y * 2)
        screen.blit(text, [text_x, text_y])

        # Instructions
        font = pygame.font.SysFont("serif", 30)
        text = font.render("Click anywhere to begin", True, constants.WHITE)
        text_x = SplashScreen.TEXT_X - (text.get_width() // 2)
        text_y = (SplashScreen.TEXT_Y - (text.get_height() // 2)) + (
                SplashScreen.TEXT_OFFSET_Y * 3)
        screen.blit(text, [text_x, text_y])


class Level01(Level):
    BACKGROUND = constants.LIGHT_GREY

    def __init__(self):
        # -- Level setup --
        super().__init__(Level01.BACKGROUND)

        # -- Player setup --
        self.player.hit_box = HitBox(self.player)
        self.all_sprites_list.remove(self.player)
        self.all_sprites_list.add(self.player.hit_box)
        self.all_sprites_list.add(self.player)

        # -- GameObject setup --

        # - GameObjects -
        self.object_list.add(
            GameObject("Tree", [160, 0], "images/tree.png", [60, 60]))
        self.object_list.add(
            GameObject("Tree", [320, 0], "images/tree.png", [60, 60]))

        self.object_list.add(
            GameObject("Desk", [200, 200], "images/desk_horizontal.png",
                       [120, 40]))
        self.object_list.add(
            GameObject("Chair", [235, 240], "images/chair_up.png", [50, 50]))

        self.object_list.add(
            GameObject("Desk", [200, 450], "images/desk_horizontal.png",
                       [120, 40]))
        self.object_list.add(
            GameObject("Chair", [235, 490], "images/chair_up.png", [50, 50]))

        self.object_list.add(
            GameObject("Desk", [680, 200], "images/desk_horizontal.png",
                       [120, 40]))
        self.object_list.add(
            GameObject("Chair", [715, 240], "images/chair_up.png", [50, 50]))

        self.object_list.add(
            GameObject("Desk", [680, 450], "images/desk_horizontal.png",
                       [120, 40]))
        self.object_list.add(
            GameObject("Chair", [715, 490], "images/chair_up.png", [50, 50]))

        self.object_list.add(
            GameObject("Trash", [700, 0], "images/trash.png", [40, 40]))

        # Water cooler is not really openable, but I wanted it to have a sound
        self.interactable_list.add(
            Openable("Water Cooler", [250, 5], "images/waterjug.png", [40, 40],
                     self.player,
                     3000, "sounds/water.wav"))

        # - Items -
        self.interactable_list.add(
            Item("Screwdriver", [200, 500], "images/screwdriver.png", [30, 30],
                 self.player))

        # - Interactables -

        # -- Door and key --
        door = Door(self.player)
        door.key.rect.x = Level.OFFSCREEN_POS[0]
        door.key.rect.y = Level.OFFSCREEN_POS[1]
        self.interactable_list.add(door)
        self.interactable_list.add(door.key)

        # - Openables and respective objects -
        self.interactable_list.add(Cabinet([0, 0], self.player))
        self.interactable_list.add(Cabinet([0, 180], self.player))
        self.interactable_list.add(Cabinet([0, 360], self.player))
        self.interactable_list.add(Cabinet([0, 540], self.player))

        # The key is hidden in this cabinet
        cabinet = Cabinet([960, 0], self.player, False, door.key)
        self.interactable_list.add(cabinet)

        self.interactable_list.add(Cabinet([960, 180], self.player))
        self.interactable_list.add(Cabinet([960, 360], self.player))
        self.interactable_list.add(Cabinet([960, 540], self.player))

        self.object_list.add(self.interactable_list)

        # Add all of the sprites to the master list
        self.all_sprites_list.add(self.object_list)


class Level02(Level):
    BACKGROUND = constants.TAN

    def __init__(self):
        # -- Level setup --
        super().__init__(Level02.BACKGROUND)

        # -- Player setup --
        self.player.hit_box = HitBox(self.player)
        self.all_sprites_list.remove(self.player)
        self.all_sprites_list.add(self.player.hit_box)
        self.all_sprites_list.add(self.player)

        # -- GameObject setup --

        # - GameObjects -
        self.object_list.add(
            GameObject("Desk", [0, 30], "images/desk_vertical.png", [40, 120]))
        self.object_list.add(
            GameObject("Chair", [40, 65], "images/chair_left.png", [50, 50]))

        self.object_list.add(
            GameObject("Desk", [0, 180], "images/desk_vertical.png",
                       [40, 120]))
        self.object_list.add(
            GameObject("Chair", [40, 215], "images/chair_left.png", [50, 50]))

        self.object_list.add(
            GameObject("Desk", [0, 330], "images/desk_vertical.png",
                       [40, 120]))
        self.object_list.add(
            GameObject("Chair", [40, 365], "images/chair_left.png", [50, 50]))

        self.object_list.add(
            GameObject("Desk", [0, 480], "images/desk_vertical.png",
                       [40, 120]))
        self.object_list.add(
            GameObject("Chair", [40, 515], "images/chair_left.png", [50, 50]))

        self.object_list.add(
            GameObject("Wall", [300, 200], "images/wall.jpeg", [60, 420]))

        self.object_list.add(
            GameObject("Table", [600, 200], "images/table.png", [200, 300]))

        self.object_list.add(
            GameObject("Counter", [950, 200], "images/counter.png", [50, 150]))
        self.object_list.add(
            GameObject("Fruit", [955, 250], "images/fruit.png", [40, 40]))
        self.interactable_list.add(
            Openable("Sink", [950, 350], "images/sink.png", [50, 50],
                     self.player, 1000,
                     "sounds/sink.wav"))
        self.object_list.add(
            GameObject("Counter", [950, 400], "images/counter.png", [50, 150]))

        self.object_list.add(
            GameObject("Trash", [955, 0], "images/trash.png", [40, 40]))

        # - Items -

        # - Interactables -

        # -- Door and key --
        door = Door(self.player)
        door.key.rect.x = Level.OFFSCREEN_POS[0]
        door.key.rect.y = Level.OFFSCREEN_POS[1]
        self.interactable_list.add(door)
        self.interactable_list.add(door.key)

        # - Openables and respective objects -

        # The safe holds the key, and the player must have the combination to
        # unlock it
        paper = Item("Safe Combo", Level.OFFSCREEN_POS, "images/safecombo.png",
                     Level.NO_SIZE, self.player)
        safe = Safe([240, 560], self.player, door.key, paper)
        fridge = Openable("Fridge", [945, 150], "images/fridge.png", [55, 50],
                          self.player, 500, "sounds/paper.wav",
                          paper)
        self.interactable_list.add(paper)
        self.interactable_list.add(safe)
        self.interactable_list.add(fridge)

        self.object_list.add(self.interactable_list)

        # Add all of the sprites to the master list
        self.all_sprites_list.add(self.object_list)


class Level03(Level):
    BACKGROUND = "images/hardwood.jpg"

    def __init__(self):
        # -- Level setup --
        super().__init__(Level03.BACKGROUND)

        # -- Player setup --
        self.player.hit_box = HitBox(self.player)
        self.all_sprites_list.remove(self.player)
        self.all_sprites_list.add(self.player.hit_box)
        self.all_sprites_list.add(self.player)

        # -- GameObject setup --

        # - Door and key -
        door = Door(self.player)
        door.key.rect.x = Level.OFFSCREEN_POS[0]
        door.key.rect.y = Level.OFFSCREEN_POS[1]
        self.interactable_list.add(door)
        self.interactable_list.add(door.key)

        # Keycards and the safe are setup prior so keycards can be hidden
        # behind other objects
        keycard_safe = KeycardSafe([450, 570], self.player, door.key)
        self.interactable_list.add(keycard_safe)

        # Blue card is hidden in the poster next to the TV
        blue_keycard = Keycard(Level.OFFSCREEN_POS, "images/keycard_blue.png",
                               self.player)
        self.interactable_list.add(blue_keycard)
        keycard_safe.keycards.append(blue_keycard)

        # Red card is hidden under a chair in the bottom left
        keycard = Keycard([95, 558], "images/keycard_red.png", self.player)
        self.interactable_list.add(keycard)
        keycard_safe.keycards.append(keycard)

        # Green card is hidden behind a tree on the left side
        keycard = Keycard([20, 85], "images/keycard_green.png", self.player)
        self.interactable_list.add(keycard)
        keycard_safe.keycards.append(keycard)

        # Yellow card is hidden in the top right cabinet
        yellow_keycard = Keycard(Level.OFFSCREEN_POS,
                                 "images/keycard_yellow.png", self.player)
        self.interactable_list.add(yellow_keycard)
        keycard_safe.keycards.append(yellow_keycard)

        # - GameObjects -
        self.object_list.add(
            GameObject("Tree", [15, 80], "images/tree.png", [60, 60]))
        self.object_list.add(
            GameObject("Reception Desk", [0, 80], "images/reception.png",
                       [220, 300]))

        self.object_list.add(
            GameObject("Armchair", [0, 410], "images/armchair_right.png",
                       [60, 60]))
        self.object_list.add(
            GameObject("Armchair", [0, 480], "images/armchair_right.png",
                       [60, 60]))
        self.object_list.add(
            GameObject("Corner Table", [0, 550], "images/corner_table.png",
                       [70, 70]))
        self.object_list.add(
            GameObject("Armchair", [90, 560], "images/armchair_up.png",
                       [60, 60]))
        self.object_list.add(
            GameObject("Armchair", [160, 560], "images/armchair_up.png",
                       [60, 60]))

        self.object_list.add(
            GameObject("Wall", [800, 100], "images/wall.jpeg", [30, 320]))

        self.object_list.add(
            GameObject("Trash", [955, 0], "images/trash.png", [40, 40]))

        # - Items -

        # - Interactables -
        self.interactable_list.add(TV([785, 220], self.player))

        # - Openables and respective objects -
        self.interactable_list.add(
            Poster([790, 120], self.player, blue_keycard))

        self.interactable_list.add(Cabinet([960, 220], self.player))
        self.interactable_list.add(Cabinet([960, 400], self.player))

        self.interactable_list.add(Cabinet([740, 580], self.player, True))
        self.interactable_list.add(
            Cabinet([920, 580], self.player, True, yellow_keycard))

        # Add all of the sprites to the master list
        self.all_sprites_list.add(self.interactable_list)
        self.all_sprites_list.add(self.object_list)

        self.object_list.add(self.interactable_list)


class EndScreen(Level):
    TEXT_X = constants.SCREEN_WIDTH // 2
    TEXT_Y = (constants.SCREEN_HEIGHT // 2) - 100
    TEXT_OFFSET_Y = 80

    def __init__(self):
        super().__init__(constants.WHITE)
        self.background = pygame.image.load("images/background.jpg")
        self.background = pygame.transform.scale(self.background, (
            constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.rect = self.background.get_rect()

        # Font is initalized here due to a bug where an error occurs in the
        # draw method if the font is not initalized
        pygame.font.init()

    def draw(self, screen):
        # Background image
        screen.fill(constants.WHITE)
        screen.blit(self.background, self.rect)

        # Game over
        font = pygame.font.SysFont("serif", 75)
        text = font.render("You have escaped! Congratulations.", True,
                           constants.WHITE)
        text_x = SplashScreen.TEXT_X - (text.get_width() // 2)
        text_y = SplashScreen.TEXT_Y - (text.get_height() // 2)
        screen.blit(text, [text_x, text_y])

        # Author
        font = pygame.font.SysFont("serif", 40)
        text = font.render("Thanks for playing :)", True, constants.WHITE)
        text_x = SplashScreen.TEXT_X - (text.get_width() // 2)
        text_y = (SplashScreen.TEXT_Y - (
                text.get_height() // 2)) + SplashScreen.TEXT_OFFSET_Y
        screen.blit(text, [text_x, text_y])

        # Instructions
        font = pygame.font.SysFont("serif", 30)
        text = font.render("Click anywhere to exit", True, constants.WHITE)
        text_x = SplashScreen.TEXT_X - (text.get_width() // 2)
        text_y = (SplashScreen.TEXT_Y - (text.get_height() // 2)) + (
                SplashScreen.TEXT_OFFSET_Y * 3)
        screen.blit(text, [text_x, text_y])
