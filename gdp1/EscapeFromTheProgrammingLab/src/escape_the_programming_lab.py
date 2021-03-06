import pygame
from Player import Player
from Level import SplashScreen, Level01, Level02, Level03, EndScreen
import constants

"""
Escape From the Programming Lab
Author: Brendan Van Allen
Version: 0.3 (beta)

How to Play:
- Move the player using the arrow keys
- Interact with items by getting close to them (practically touching them), and
  pressing Enter

Objective:
- Find the key that unlocks the door for each level

Credits:
- The hierarchy of how the game runs (main, Game, Level) is taken directly from
  http://programarcadegames.com/
- Background music from: http://www.bensound.com
- Sound effects from: https://zapsplat.com
- Images courtesy of Google.
"""


# Game contains the infrastructure for running the game, switching levels, etc.
class Game(object):
    NO_INTERACT_SOUND = pygame.mixer.Sound("sounds/no_interact.wav")
    ESCAPE_SOUND = pygame.mixer.Sound("sounds/cheers.wav")

    def __init__(self):
        self.game_start = False
        self.game_over = False

        # Create the player
        self.player = Player()

        # Create the levels
        self.level_list = []
        self.level_list.append(SplashScreen())
        self.level_list.append(Level01())
        self.level_list.append(Level02())
        self.level_list.append(Level03())
        self.level_list.append(EndScreen())

        # Set the current level
        self.current_level_num = 0
        self.current_level = self.level_list[self.current_level_num]
        self.player = self.current_level.player
        self.player.level = self.current_level

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Only register for splash screen and end screen
                if self.current_level_num == 0 or \
                   self.current_level_num == len(self.level_list)-1:
                    self.current_level.complete = True

            if event.type == pygame.KEYDOWN:
                # Movement keys
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                if event.key == pygame.K_RIGHT:
                    self.player.go_right()
                if event.key == pygame.K_UP:
                    self.player.go_up()
                if event.key == pygame.K_DOWN:
                    self.player.go_down()

                # Interaction keys
                if event.key == pygame.K_RETURN:
                    if 0 < self.current_level_num < len(self.level_list)-1:
                        interacted = self.player.interact()
                        if not interacted:
                            Game.NO_INTERACT_SOUND.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop_x()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop_x()
                if event.key == pygame.K_UP and self.player.change_y < 0:
                    self.player.stop_y()
                if event.key == pygame.K_DOWN and self.player.change_y > 0:
                    self.player.stop_y()

        return False

    def run_logic(self):
        if not self.current_level.complete:
            self.current_level.update()
        else:
            # Switch to the next level, or end the game
            self.current_level_num += 1
            if self.current_level_num < len(self.level_list):
                self.current_level = self.level_list[self.current_level_num]
                self.player = self.current_level.player
                self.player.level = self.current_level

                # If player beats the game, stop music and play victory sound
                if self.current_level_num == len(self.level_list)-1:
                    pygame.mixer_music.stop()
                    Game.ESCAPE_SOUND.play()
                elif self.current_level_num-1 != 0:
                    # Wait for door animation
                    pygame.time.wait(3000)
            else:
                self.game_over = True

    def display_frame(self, screen):
        screen.fill(constants.WHITE)
        self.current_level.draw(screen)
        pygame.display.flip()


def main():
    # Initialize Pygame and set up the window
    pygame.init()

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Escape the Programming Lab")
    pygame.mouse.set_visible(False)

    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    # Start the music and don't let it stop
    pygame.mixer_music.load("sounds/scifi.mp3")
    pygame.mixer_music.set_volume(0.5)
    pygame.mixer_music.play(-1)

    # Main game loop
    while not done:

        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

        if game.game_over:
            done = True

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
