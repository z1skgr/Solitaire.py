"""
----------------------------------------------------------------------------------------------------
InterstitialState

Displays a message between screens. Can be used for ''Game over'' or ''Get ready'' style
messages
----------------------------------------------------------------------------------------------------
"""
from mode1 import Cards, SolitaireGame
from mode1.Bitmapfont import BitmapFont
from mode1.Raspigame import GameState


class InterstitialState(GameState):

    def __init__(self, game, msg, waitTimeMs, nextState):
        super(InterstitialState, self).__init__(game)
        self.nextState = nextState
        self.font = BitmapFont('fasttracker2-style_12x12.png', 12, 12)
        self.message = msg
        self.waitTimer = waitTimeMs

    def update(self, gameTime):
        self.waitTimer -= gameTime
        if self.waitTimer < 0:
            self.game.changeState(self.nextState)

    def draw(self, surface):
        self.font.centre(surface, self.message, surface.get_rect().height / 2)
        self.font.centre(surface, " Score:" + str(Cards.score), (surface.get_rect().height / 2) + 20)
        self.font.centre(surface, " Moves:" + str(Cards.moves), (surface.get_rect().height / 2) + 40)
        self.font.centre(surface, str(SolitaireGame.output_string), (surface.get_rect().height / 2) + 60)


