import pygame
import constants


# A generic object that the player can't move over, but doesn't do anything.
class GameObject(pygame.sprite.Sprite):
    def __init__(self, name, position, image_file, size):
        super().__init__()

        self.name = name
        self.position = position
        self.image = pygame.image.load(image_file)

        # Resize the image
        self.image = pygame.transform.scale(self.image, size)
        self.image.convert_alpha()

        # Set the position
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]


# An object that can be interacted with to do something
class Interactable(GameObject):
    def __init__(self, name, position, image_file, size, player, wait_time):
        super().__init__(name, position, image_file, size)
        self.player = player
        self.wait_time = wait_time

    # This method should be overwritten in each subclass to peform the specific
    # function required by that class
    def interact(self):
        print("Player interacted with: " + self.name)


# An object that can contain an item and can be opened to pickup the item
class Openable(Interactable):
    def __init__(self, name, position, image_file, size, player, wait_time,
                 sound_file, item=None):
        super().__init__(name, position, image_file, size, player, wait_time)

        self.sound = pygame.mixer.Sound(sound_file)
        self.item = item

    def interact(self):
        # 'Opens' this object and if it contains an item, the item is put in
        # the player's inventory
        if self.item is not None:
            self.player.pickup(self.item)
            self.item = None

        # Sound will always play when opening this object, even if there is no
        # item inside
        self.sound.play()

        return self.wait_time


# A generic cabinet that can contain an item
class Cabinet(Openable):
    def __init__(self, position, player, rotate=False, item=None):
        name = "Cabinet"
        size = (40, 80)
        image_file = "images/cabinet.png"

        if rotate:
            size = (80, 40)
            image_file = "images/cabinet_rotate.png"

        wait_time = 1000
        sound_file = "sounds/cabinet_open.wav"
        super().__init__(name, position, image_file, size, player, wait_time,
                         sound_file, item)


# A tv that simply turns on and off when interacted with
class TV(Interactable):
    ON_IMAGE = pygame.image.load("images/tv_on.png")
    OFF_IMAGE = pygame.image.load("images/tv.png")

    def __init__(self, position, player):
        name = "TV"
        self.size = [15, 100]
        image_file = "images/tv.png"
        wait_time = 200
        super().__init__(name, position, image_file, self.size, player,
                         wait_time)

        TV.ON_IMAGE = pygame.transform.scale(TV.ON_IMAGE, self.size).\
            convert_alpha()
        TV.OFF_IMAGE = pygame.transform.scale(TV.OFF_IMAGE, self.size).\
            convert_alpha()

        self.on = False

    def interact(self):
        self.on = not self.on
        return self.wait_time

    def update(self):
        if self.on:
            self.image = pygame.transform.scale(TV.ON_IMAGE, self.size).\
                convert_alpha()
        else:
            self.image = pygame.transform.scale(TV.OFF_IMAGE, self.size).\
                convert_alpha()


# Door is on each level and is how the player escapes
class Door(Interactable):
    pygame.mixer.init()
    OPEN_SOUND = pygame.mixer.Sound("sounds/door_open.wav")

    def __init__(self, player):
        name = "Door"
        width = 100
        height = 20
        position = (constants.SCREEN_WIDTH // 2 - width // 2, 0)
        image_file = "images/door.png"
        size = (width, height)
        wait_time = 3
        super().__init__(name, position, image_file, size, player, wait_time)

        # Key position is updated in each level's constructor
        self.key = Item("Key", [0, 0], "images/key.png", [20, 20], player)

    def interact(self):
        # Open the door if the player has the key
        if self.key in self.player.inventory.items:
            Door.OPEN_SOUND.play()
            return True

        return False


# A simple safe that contains an item and requires a combination to be opened
class Safe(Openable):
    OPEN_SOUND = pygame.mixer.Sound("sounds/safe_door.wav")
    LOCKED_SOUND = pygame.mixer.Sound("sounds/locked_safe.wav")
    LOCK_DIAL_SOUND = pygame.mixer.Sound("sounds/lock_dial.wav")

    def __init__(self, position, player, item, combination):
        name = "Safe"
        image_file = "images/safe.png"
        size = (60, 60)
        wait_time = 1000
        sound_file = Safe.OPEN_SOUND
        self.combination = combination
        self.opened = False

        super().__init__(name, position, image_file, size, player, wait_time,
                         sound_file, item)

    def interact(self):
        if not self.opened:
            # Open the safe if the player has the combination
            if self.combination in self.player.inventory.items:
                Safe.LOCK_DIAL_SOUND.play()
                pygame.time.wait(3000)
                super().interact()
                self.opened = True
            else:
                Safe.LOCKED_SOUND.play()
        else:
            Safe.OPEN_SOUND.play()

        return self.wait_time


# A keycard cafe that contains an item and requires 4 keycards to be opened
class KeycardSafe(Openable):
    OPEN_SOUND = pygame.mixer.Sound("sounds/keysafe_open.wav")
    LOCKED_SOUND = pygame.mixer.Sound("sounds/locked_safe.wav")
    SCAN_SOUND = pygame.mixer.Sound("sounds/scan.wav")
    ClOSE_SOUND = pygame.mixer.Sound("sounds/keysafe_close.wav")

    OPEN_IMAGE = pygame.image.load("images/keysafe_open.png")
    CLOSED_IMAGE = pygame.image.load("images/keysafe_closed.png")

    def __init__(self, position, player, item):
        name = "Safe"
        image_file = "images/keysafe_closed.png"
        size = (100, 50)
        wait_time = 1000
        sound_file = KeycardSafe.OPEN_SOUND
        super().__init__(name, position, image_file, size, player, wait_time,
                         sound_file, item)

        # Size images
        KeycardSafe.OPEN_IMAGE = pygame.transform.scale(KeycardSafe.OPEN_IMAGE,
                                                        size).convert_alpha()
        KeycardSafe.CLOSED_IMAGE = pygame.transform.scale(
            KeycardSafe.CLOSED_IMAGE, size).convert_alpha()

        # Keycards are added in the Level construction
        self.keycards = []

        # Contains the keycards already scanned
        self.scanned = []

        # Flag for if a card was scanned or not
        self.no_scan = True

        # Flag for if the safe was interacted with (used to update image)
        self.interacted = False

        # Counts frames to aid animation of opening
        self.frame_count = 0

        self.opened = False

    def interact(self):
        if not self.opened:
            self.no_scan = True
            for key in self.keycards:
                if key in self.player.inventory.items \
                        and key not in self.scanned:
                    self.no_scan = False
                    self.scanned.append(key)
                    self.player.inventory.remove(key)
                    KeycardSafe.SCAN_SOUND.play()
                    self.wait_time = 1000

                    if len(self.scanned) == len(self.keycards):
                        self.opened = True
                        pygame.time.wait(self.wait_time)

                    # Break limits scanning to one card at a time
                    break

            # Safe is still locked and player interacted with no keycards
            if self.no_scan:
                Safe.LOCKED_SOUND.play()
                self.wait_time = 3000

        # Open the safe if it was opened
        if self.opened:
            super().interact()
            self.opened = True
            self.interacted = True
            self.wait_time = 2000

        return self.wait_time

    def update(self):
        if self.interacted:
            self.image = pygame.transform.scale(KeycardSafe.OPEN_IMAGE,
                                                (100, 50)).convert_alpha()
            self.frame_count += 1

            if self.frame_count >= 60:
                KeycardSafe.ClOSE_SOUND.play()
                pygame.time.wait(200)
                self.image = pygame.transform.scale(KeycardSafe.CLOSED_IMAGE,
                                                    (100, 50)).convert_alpha()
                self.interacted = False
                self.frame_count = 0


# A simple poster that can be ripped to reveal an item
class Poster(Openable):
    RIPPED_IMAGE_CARD = pygame.image.load("images/poster_ripped_bluecard.png")
    RIPPED_IMAGE = pygame.image.load("images/poster_ripped.png")

    def __init__(self, position, player, item):
        name = "Safe"
        image_file = "images/poster.png"
        size = (10, 60)
        wait_time = 300
        sound_file = "sounds/paper.wav"
        super().__init__(name, position, image_file, size, player, wait_time,
                         sound_file, item)

        Poster.RIPPED_IMAGE_CARD = pygame.transform.scale(
            Poster.RIPPED_IMAGE_CARD, size).convert_alpha()
        Poster.RIPPED_IMAGE = pygame.transform.scale(
            Poster.RIPPED_IMAGE, size).convert_alpha()

        self.ripped = False

    def interact(self):
        if not self.ripped:
            # Rip the poster to reveal the item
            self.image = Poster.RIPPED_IMAGE_CARD.convert_alpha()
            self.sound.play()
            self.ripped = True
        else:
            # If card is still there, pick it up
            if self.item is not None:
                self.image = Poster.RIPPED_IMAGE
                Item.PICKUP_SOUND.play()
                self.player.pickup(self.item)
                self.item = None

        return self.wait_time


# A generic item that can be picked up by the player
class Item(Interactable):
    PICKUP_SOUND = pygame.mixer.Sound("sounds/item_pickup.wav")

    def __init__(self, name, position, image_file, size, player):
        wait_time = 300
        super().__init__(name, position, image_file, size, player, wait_time)

    def interact(self):
        self.player.pickup(self)
        Item.PICKUP_SOUND.play()
        return self.wait_time


class Keycard(Item):
    def __init__(self, position, image_file, player):
        name = "Keycard"
        size = [30, 15]
        super().__init__(name, position, image_file, size, player)
