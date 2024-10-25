import pygame
import sys

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

    def onEnter(self, previousState): # Placeholder for actions to perform when entering this state
        pass

    """
    Called by the game when leaving the state.
    """

    def onExit(self): # Placeholder for actions to perform when exiting this state
        pass

    """
    Called by the game allowing the state to update itself. The game time (in milliseconds) since
    the last call is passed.
    """

    def update(self, gameTime): # Placeholder for updating the state based on game time
        pass

    def update_onPress(self, gameTime, value): # Placeholder for handling mouse button press events
        pass

    def update_onRelease(self, gameTime): # Placeholder for handling mouse button release events
        pass

    def getIndex(self, gameTime): # Placeholder for retrieving the index of the current state
        pass

    def button(self): # Placeholder for button-related functionality
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

        self.fpsClock = pygame.time.Clock() # Create a clock to manage the frame rate
        self.main_window = pygame.display.set_mode((width, height)) # Set the dimensions of the game window
        self.background = pygame.Color(255, 255, 255) # Set the initial background color to white
        self.currentState = None
        self.game_over = False # Flag to indicate if the game is over
        self.done = False # Flag to indicate if the game loop should continue


    """
    Change the current state. If the newState is 'None' then the game will terminate.
    """

    def changeState(self, newState):
        if self.currentState is not None:
            self.currentState.onExit()

        if newState is None:
            pygame.quit()
            sys.exit()

        old_state = self.currentState
        self.currentState = newState
        newState.onEnter(old_state)

    """
    Run the game. Initial state must be supplied.
    """

    def run(self, initialState):
        self.changeState(initialState)
        value = 0
        gameTime = 0


        while not self.done:

            if self.currentState.getIndex(gameTime) is not None:
                value = self.currentState.getIndex(gameTime)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_q):  # # If user presses 'q' or closes the window, quit the game:
                    self.done = True
                    pygame.quit() # Quit pygame
                    sys.exit()


                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.currentState.update_onPress(gameTime, value)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.currentState.update_onRelease(gameTime)

            gameTime = self.fpsClock.get_time() # Update game time

            if self.currentState is not None: # Update the current state
                self.currentState.update(gameTime)


            self.main_window.fill(self.background)
            bimage = pygame.image.load('background.png') # Load the background image
            self.main_window.blit(bimage, (0, 0)) # Draw the background image on the window
            if self.currentState is not None:
                self.currentState.draw(self.main_window) # Draw the current state on the window

            pygame.display.flip() # Update the display
            self.fpsClock.tick(20) # Control the frame rate to 20 FPS

        pygame.quit() # Quit pygame when the loop ends

