import pygame
import sys
from pygame.locals import *

"""----------------------------------------------------------------------------------------------------
GameState
The game state class defines an interface that is used by the RaspberryPiGame class. Each state
manages a particular function of the game. For example; main menu, the actual game play, and
interstitial screens.
----------------------------------------------------------------------------------------------------
"""


class GameState(object):
    """
    Initialise the Game state class. Each sub-type must call this method. Takes one parameter, which
    is the game instance.
    """

    def __init__(self, game):
        self.game = game

    """
    Called by the game when entering the state for the first time.
    """

    def onEnter(self, previousState):
        pass

    """
    Called by the game when leaving the state.
    """

    def onExit(self):
        pass

    """
    Called by the game allowing the state to update itself. The game time (in milliseconds) since
    the last call is passed.
    """

    def update(self, gameTime):
        pass

    def update_onPress(self, gameTime, value):
        pass

    def update_onRelease(self, gameTime):
        pass

    def indfun(self, gameTime):
        pass

    def button(self):
        pass

    """
    Called by the game allowing the state to draw itself. The surface that is passed is the
    current drawing surface.
    """

    def draw(self, surface):
        pass



"""
----------------------------------------------------------------------------------------------------
Raspberry Pi Game

Basic game object-oriented framework for the Raspberry Pi. Users create 'states' that alter what is
being displayed on-screen / updated at any particular time.
----------------------------------------------------------------------------------------------------
"""


class RaspberryPiGame(object):
    """
    Initialise the Raspberry Pi Game class.
    """

    def __init__(self, gameName, width, height):

        pygame.init()
        pygame.display.set_caption(gameName)

        self.fpsClock = pygame.time.Clock()
        self.mainwindow = pygame.display.set_mode((width, height))
        self.background = pygame.Color(255, 255, 255)
        self.currentState = None
        self.gameover = False
        self.done = False
        self.restart = False

    """
    Change the current state. If the newState is 'None' then the game will terminate.
    """

    def changeState(self, newState):
        if self.currentState is not None:
            self.currentState.onExit()

        if newState is None:
            pygame.quit()
            sys.exit()

        oldState = self.currentState
        self.currentState = newState
        newState.onEnter(oldState)

    """
    Run the game. Initial state must be supplied.
    """

    def run(self, initialState):
        self.changeState(initialState)
        value = 0
        gameTime = 0


        while not self.done:
            #print(gameTime)
            # Edw ginete gnwsto to mode pou dialexame
            # if not isinstance(self.currentState, InterstitialState) and not isinstance(self.currentState,
            #                                                                          PlayGameState):
            #  value = self.currentState.index

            # if isinstance(self.currentState, PlayGameState):
            #   print(isinstance(self.currentState, PlayGameState))

            if self.currentState.indfun(gameTime) is not None:
                value = self.currentState.indfun(gameTime)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_q):  # If user
                    self.done = True  # clicked close:
                    pygame.quit()
                    sys.exit()

                    # new lines to make it set restart to true if r is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.done = True


                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.currentState.update_onPress(gameTime, value)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.currentState.update_onRelease(gameTime)

            gameTime = self.fpsClock.get_time()

            if self.currentState is not None:
                self.currentState.update(gameTime)


            self.mainwindow.fill(self.background)
            bimage = pygame.image.load('background.png')
            self.mainwindow.blit(bimage, (0,0))
            if self.currentState is not None:
                self.currentState.draw(self.mainwindow)

            pygame.display.flip()
            self.fpsClock.tick(20)

        pygame.quit()
        # print(self.restart)

# def restartf(self):
#    if __name__ == '__main__':
#       pass
#  else:
#     while self.run(self.currentState):
#        self.currentState.m_card = []
