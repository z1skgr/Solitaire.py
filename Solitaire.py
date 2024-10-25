# Our imports

import math

from Interstitial import *
from MainMenu import MainMenuState
from Raspigame import RaspberryPiGame
from SolitaireGame import PlayGameState

"""----------------------------------------------------------------------------------------------------
Application Entry Point Main entry point to the application. Sets up the objects and starts the main loop.
----------------------------------------------------------------------------------------------------
"""

solitaireGame = RaspberryPiGame("Solitaire", 800, 600)
mainMenuState = MainMenuState(solitaireGame)
endState = InterstitialState(solitaireGame, 'Congratulations!!!', math.inf, mainMenuState)
failState = InterstitialState(solitaireGame, "Try Again!", math.inf, mainMenuState)
playGameState = PlayGameState(solitaireGame, endState, failState)
getReadyState = InterstitialState(solitaireGame, 'Get Ready#!', 2000, playGameState)
mainMenuState.setPlayState(getReadyState)


solitaireGame.run(mainMenuState)

