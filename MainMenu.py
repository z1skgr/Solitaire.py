import pygame
from pygame.locals import *

from Bitmapfont import BitmapFont
from Raspigame import GameState


class MainMenuState(GameState):

    def __init__(self, game):
        super(MainMenuState, self).__init__(game)
        self.playGameState = None # Initialize playGameState to None
        self.font = BitmapFont('fasttracker2-style_12x12.png', 12, 12)
        self.index = 0
        self.inputTick = 0
        self.menuItems = ['Start Game - Draw 1', 'Start Game - Draw 3', 'Quit'] # Define menu items

    def setPlayState(self, state): # Method to set the play state
        self.playGameState = state

    def getIndex(self, gameTime): # Method to get the current index
        return self.index

    def update(self, gameTime): # Method to update the menu state

        keys = pygame.key.get_pressed()
        if (keys[K_UP] or keys[K_DOWN]) and self.inputTick == 0:
            self.inputTick = 250
            if keys[K_UP]: # If the up key is pressed
                self.index -= 1 # Handle menu choices up and down
                if self.index < 0:
                    self.index = len(self.menuItems) - 1
            elif keys[K_DOWN]:
                self.index += 1
                if self.index == len(self.menuItems):
                    self.index = 0
        elif self.inputTick > 0:
            self.inputTick -= gameTime

        if self.inputTick < 0:
            self.inputTick = 0

        if keys[K_SPACE]: # If the space key is pressed
            if self.index == 2: # If the index is 2 (Quit)
                self.game.changeState(None)  # Exit the game
            else:
                self.game.changeState(self.playGameState)  # Start game

    # Method to draw the menu on the screen
    def draw(self, surface):
        self.font.centre(surface, "Solitaire Game!", 48) # Center the title on the surface
        count = 0
        y = surface.get_rect().height - len(self.menuItems) * 160 # Calculate starting y position for menu items
        for item in self.menuItems:
            itemText = "  "

            if count == self.index:
                itemText = "> "

            itemText += item
            self.font.draw(surface, itemText, 25, y)
            y += 24
            count += 1 # Increment count for the next iteration
