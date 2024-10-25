"""
----------------------------------------------------------------------------------------------------
InterstitialState

Displays a message between screens. Can be used for ''Game over'' or ''Get ready'' style
messages
----------------------------------------------------------------------------------------------------
"""
import Cards
import SolitaireGame
from Bitmapfont import BitmapFont
from Raspigame import GameState


class InterstitialState(GameState):

    def __init__(self, game, msg, waitTimeMs, nextState):
        super(InterstitialState, self).__init__(game)
        self.nextState = nextState
        self.font = BitmapFont('fasttracker2-style_12x12.png', 12, 12)
        self.message = msg # Storing the message to be displayed
        self.waitTimer = waitTimeMs # Setting the timer for how long to wait before transitioning

    def update(self, gameTime):
        self.waitTimer -= gameTime
        if self.waitTimer < 0:
            self.game.changeState(self.nextState) # Changing to the next game state

    def draw(self, surface):
        self.font.centre(surface, self.message, surface.get_rect().height / 2)
        self.font.centre(surface, " Score:" + str(Cards.score), (surface.get_rect().height / 2) + 20)
        self.font.centre(surface, " Moves:" + str(Cards.moves), (surface.get_rect().height / 2) + 40)
        self.font.centre(surface, str(SolitaireGame.output_string), (surface.get_rect().height / 2) + 60)


