import pygame
import constants
from GameObject import Interactable, Door
from Spritesheet import Spritesheet


class Player(pygame.sprite.Sprite):
    SPEED = 7
    WIDTH = 70
    HEIGHT = 70

    def __init__(self):
        super().__init__()

        # Setup the spritesheets and image sets
        # Image sets are indexed for images in the order: 0 - stopped,
        # 1 - walking 1/interacting, 2 - walking 2
        spritesheet = Spritesheet("images/player_up.png")
        self.images_up = spritesheet.images_at(([0, 0, 80, 65],
                                                [160, 0, 80, 65],
                                                [400, 0, 80, 65]))

        spritesheet = Spritesheet("images/player_down.png")
        self.images_down = spritesheet.images_at(([400, 0, 80, 65],
                                                  [240, 0, 80, 65],
                                                  [0, 0, 80, 65]))

        spritesheet = Spritesheet("images/player_right.png")
        self.images_right = spritesheet.images_at(([0, 0, 65, 80],
                                                   [0, 160, 65, 80],
                                                   [0, 400, 65, 80]))

        spritesheet = Spritesheet("images/player_left.png")
        self.images_left = spritesheet.images_at(([0, 400, 65, 80],
                                                  [0, 240, 65, 80],
                                                  [0, 0, 65, 80]))

        # Set the initial image to standing still
        self.image = self.images_up[0]
        self.image = pygame.transform.scale(self.image,
                                            (Player.WIDTH, Player.HEIGHT))
        self.rect = self.image.get_rect()

        # This will hold the current image set based on the last direction the
        # player moved in
        self.image_set = self.images_up

        # A counter used to time animations
        self.frame_count = 0
        self.image_index = 0

        # Center the player on the game screen (height does not include
        # inventory space)
        self.rect.x = constants.SCREEN_WIDTH // 2 - Player.WIDTH // 2
        self.rect.y = \
            (constants.SCREEN_HEIGHT - Inventory.HEIGHT) // 2 - \
            Player.HEIGHT // 2

        # Player does not move until controlled
        self.change_x = 0
        self.change_y = 0
        self.moving = False

        # Level is set in Game
        self.level = None

        # The hit box is set in each level's constructor so that its color
        # matches the background of that level
        self.hit_box = None

        self.interacting = False
        self.wait_time = 0
        self.door_opened = False

        self.inventory = Inventory()

    def update(self):
        # Update the player position
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Update the player image
        if self.moving:
            # Switch the player image every 5 frames to simulate walking
            if self.frame_count <= 10:
                self.image = self.image_set[1]
            else:
                self.image = self.image_set[2]
                if self.frame_count >= 20:
                    self.frame_count = 0
        elif self.interacting:
            self.image = self.image_set[1]
            if self.frame_count >= 1:
                pygame.time.wait(self.wait_time)
                self.frame_count = 0
                self.interacting = False
        else:
            self.image = self.image_set[0]
            self.frame_count = 0

        self.image = pygame.transform.scale(self.image,
                                            (Player.WIDTH, Player.HEIGHT))
        self.image.convert_alpha()
        self.frame_count += 1

        # Reset to last position if the move would put the player off the
        # screen, or into the inventory space
        if self.rect.x < 0 or self.rect.right > constants.SCREEN_WIDTH:
            self.rect.x -= self.change_x
        if self.rect.y < 0 or self.rect.bottom > (constants.SCREEN_HEIGHT -
                                                  Inventory.HEIGHT -
                                                  HitBox.HIT_BUFFER):
            self.rect.y -= self.change_y

        # Reset to last position if the move would collide with an object
        object_hit_list = pygame.sprite.spritecollide(self,
                                                      self.level.object_list,
                                                      False)
        for obj in object_hit_list:
            # Moving right
            if self.change_x > 0:
                self.rect.right = obj.rect.left
            # Moving left
            if self.change_x < 0:
                self.rect.left = obj.rect.right
            # Moving down
            if self.change_y > 0:
                self.rect.bottom = obj.rect.top
            # Moving up
            if self.change_y < 0:
                self.rect.top = obj.rect.bottom

        if self.door_opened:
            self.level.complete = True

    def interact(self):
        # The hit box is used to determine if a player is close enough to be
        # interacted with
        object_hit_list = pygame.sprite.spritecollide(self.hit_box,
                                                      self.level.
                                                      interactable_list,
                                                      False)

        # Each level is setup so no two interactables are close enough to both
        # be interacted with at the same time
        if len(object_hit_list) > 0:
            obj = object_hit_list[0]
            if isinstance(obj, Interactable):
                if type(obj) is Door:
                    self.door_opened = obj.interact()
                else:
                    self.wait_time = obj.interact()

                self.interacting = True
                self.frame_count = 0
                return True

        # No objects interacted with
        return False

    def pickup(self, item):
        self.inventory.add(item)

        # Remove from the game screen
        self.level.object_list.remove(item)
        self.level.interactable_list.remove(item)
        self.level.all_sprites_list.remove(item)

    # Player-controlled movement:
    def go_left(self):
        self.change_x = -Player.SPEED
        self.change_y = 0
        self.image_set = self.images_left
        self.moving = True

    def go_right(self):
        self.change_x = Player.SPEED
        self.change_y = 0
        self.image_set = self.images_right
        self.moving = True

    def go_up(self):
        self.change_y = -Player.SPEED
        self.change_x = 0
        self.image_set = self.images_up
        self.moving = True

    def go_down(self):
        self.change_y = Player.SPEED
        self.change_x = 0
        self.image_set = self.images_down
        self.moving = True

    def stop_x(self):
        self.change_x = 0
        self.moving = False

    def stop_y(self):
        self.change_y = 0
        self.moving = False


class HitBox(pygame.sprite.Sprite):
    # Represents how far from each edge of the player that objects can be
    # detected
    HIT_BUFFER = 5

    def __init__(self, player):
        super().__init__()

        # Create the surface
        width = Player.WIDTH + HitBox.HIT_BUFFER * 2
        height = Player.HEIGHT + HitBox.HIT_BUFFER * 2
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image = self.image.convert_alpha(self.image)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()

        self.player = player

    def update(self):
        # Sticks to player position
        self.rect.x = self.player.rect.x - HitBox.HIT_BUFFER
        self.rect.y = self.player.rect.y - HitBox.HIT_BUFFER


class Inventory(pygame.sprite.Sprite):
    WIDTH = constants.SCREEN_WIDTH
    HEIGHT = 100
    X = 0
    Y = constants.SCREEN_HEIGHT - HEIGHT
    SLOT_X = 50
    SLOT_Y = 10
    SLOT_WIDTH = 80
    SLOT_HEIGHT = 80
    SLOT_SPACING = 100

    def __init__(self):
        super().__init__()

        self.items = []
        self.slot_index = 0

        # Background image
        self.image = pygame.Surface((Inventory.WIDTH, Inventory.HEIGHT))
        self.image.fill(constants.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = Inventory.X
        self.rect.y = Inventory.Y

        # Slot images
        for i in range(9):
            slot = pygame.Surface(
                (Inventory.SLOT_WIDTH, Inventory.SLOT_HEIGHT))
            slot.fill(constants.DARK_GREY)
            self.image.blit(slot, (
                Inventory.SLOT_X + i * Inventory.SLOT_SPACING,
                Inventory.SLOT_Y))

    def add(self, item):
        self.items.append(item)

        # Add item image to inventory surface
        item.image = pygame.transform.scale(item.image,
                                            [Inventory.SLOT_WIDTH,
                                             Inventory.SLOT_HEIGHT])
        item.rect = item.image.get_rect()
        item.rect.x = Inventory.SLOT_X + (self.slot_index *
                                          Inventory.SLOT_SPACING)
        item.rect.y = Inventory.SLOT_Y
        self.image.blit(item.image, item.rect)

        # Increase index so the next item is added to the next slot
        self.slot_index += 1

    def remove(self, item):
        self.items.remove(item)
        self.slot_index -= 1

    def update(self):
        self.image.fill(constants.BLACK)

        # Slot images
        for i in range(9):
            slot = pygame.Surface(
                (Inventory.SLOT_WIDTH, Inventory.SLOT_HEIGHT))
            slot.fill(constants.DARK_GREY)
            self.image.blit(slot, (
                Inventory.SLOT_X + i * Inventory.SLOT_SPACING,
                Inventory.SLOT_Y))

        # Items
        self.slot_index = 0
        for item in self.items:
            item.image = pygame.transform.scale(item.image,
                                                [Inventory.SLOT_WIDTH,
                                                 Inventory.SLOT_HEIGHT])
            item.rect = item.image.get_rect()
            item.rect.x = Inventory.SLOT_X + (self.slot_index *
                                              Inventory.SLOT_SPACING)
            item.rect.y = Inventory.SLOT_Y
            self.image.blit(item.image, item.rect)
            self.slot_index += 1
