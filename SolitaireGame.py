"""
Solitaire Game Implementation

This script implements a Solitaire card game using Pygame.

Authors:
    - Christos Ziskas (cziskas@gmail.com)

Last Modified: 2024-10-24

Version: 1.0

License: MIT License

Copyright (c) 2024 Christos Ziskas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


###Imports
import random

import pyautogui
from pygame.mixer import SoundType

import Cards
from Cards import *
from Raspigame import GameState
from Bitmapfont import *

# Defining color constants using RGB tuples
black = (0, 0, 0)
nblack = (128, 128, 128)
white = (255, 255, 255)
red = (200, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)
color_dark = (80,80,80)
color_light = (160,160,160)

clock = pygame.time.Clock()
frame_count = 0
frame_rate = 60
start_time = 90
total_seconds = frame_count // frame_rate
minutes = total_seconds // 60
seconds = total_seconds % 60
output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
count = 0
end = False
cards_hid = 0
movingFlag=False





# Function to alert the user when no moves are available
def auto_change():
    global end
    pyautogui.alert('No Moves Available')
    end = True

# Function to manage the game timer
def timer():
    global frame_count, frame_rate, output_string, minutes, seconds, total_seconds
    total_seconds = frame_count // frame_rate

    # Divide by 60 to get total minutes
    minutes = total_seconds // 60

    # Use modulus (remainder) to get seconds
    seconds = total_seconds % 60

    # Use python string formatting to format in leading zeros
    output_string = "TIME: {0:02}:{1:02}".format(minutes, seconds)

    frame_count += 3
    # Limit frames per second
    clock.tick(frame_rate)

# Function to play background sound
def sound():
    mixer = pygame.mixer.Sound('cas music.wav')
    pygame.mixer.Channel(0).play(mixer)
    mixer.play(-1)

# Class representing the game state during play
class PlayGameState(GameState):
    sound: SoundType

    def __init__(self, game, endState, failState):
        super(PlayGameState, self).__init__(game)
        self.deck_dict = {} # Dictionary to hold deck images
        self.deck_list = [] # List to hold the deck of cards
        self.restart = 0
        self.endState = endState
        self.failState = failState
        self.board_piles = 7 # Number of piles in board
        self.win_piles = 4 # Number of winning piles

        self.start_path = None # Path for card images
        self.final_path = None # Final path for card images
        self.m_card = None # Currently moved card
        self.card_list = [] # List of shuffled cards
        self.hints = None # Variable to hold hints

        self.font = BitmapFont('fasttracker2-style_12x12.png', 12, 12)
        self.initialise()

    # Function to initialise cards and the game board
    def initialise(self):
        global cards_hid
        self.initialise_deck()
        self.initialise_table()
        cards_hid = len(self.deck_list[0].hidden_cards)
        sound()

    # Cards initialisation and shuffling related to solitaire rules
    def initialise_deck(self):
        self.m_card = MovedCard()
        for s in ["spades", "clubs", "diamonds", "hearts"]:
            for i in range(1, 14):
                self.start_path = 'playing_cards'
                if i == 1:
                    self.start_path += '/ace_' + s + '.png'
                    self.final_path = 'ace_' + s
                elif i == 11:
                    self.start_path += '/jack_' + s + '.png'
                    self.final_path = 'jack_' + s
                elif i == 12:
                    self.start_path += '/queen_' + s + '.png'
                    self.final_path = 'queen_' + s
                elif i == 13:
                    self.start_path += '/king_' + s + '.png'
                    self.final_path = 'king_' + s
                else:
                    self.start_path += '/' + str(i) + '_' + s + '.png'
                    self.final_path = str(i) + '_' + s

                #   print(self.start_path)
                #   print(self.final_path)
                im = pygame.image.load(self.start_path).convert()
                self.deck_dict[self.final_path] = im
        self.card_list = self.shuffle_cards()


    #Table initialisation based on solitaire rules and deck layout
    def initialise_table(self):
        self.deck_list.append(Card2(130, 30))
        length = len(self.deck_list)
        for i in range(length, self.board_piles + 1):
            self.deck_list.append(Card1(30 + 100 * (i - 1), 160, i))
        for i in range(1, self.win_piles + 1):
            self.deck_list.append(Card3(330 + 100 * (i - 1), 30))

        for i in range(1, self.board_piles + 1):
            self.deck_list[i].extend_list(self.card_list[:i])
            del self.card_list[:i]

        self.deck_list[0].hidden_cards.extend(self.card_list)

    """
    Checks if all foundation piles are complete (have 13 cards each). 
    If they are, it ends the game, presumably in a victory state. 
    If any foundation pile is incomplete, the game continues.
    """
    #Every frame function to check if the game is won and change the state to endState if it is won.
    def update(self, gameTime):
        for item in self.deck_list:
            if isinstance(item, Card3): #Checking if the item is an instance of Card3. On winning pile
                if len(item.cards) != 13:
                    return False
        else:
            self.game.changeState(self.endState) # Changing the game state to endState

    def update_onPress(self, gameTime, value):
        global cards_hid, movingFlag
        #print(self.deck_list[0].hidden_cards)
        if len(self.deck_list[0].hidden_cards) == 0: # If there are no hidden cards
            self.hints = self.available_hints(value) # Getting available hints

        if len(self.deck_list[0].cards_list) == 0: # If there are no cards in the list
            cards_hid = len(self.deck_list[0].hidden_cards) # Updating cards_hid with the number of hidden cards

        #print("hint", self.hints)
        #print(self.deck_list)
        for item in self.deck_list:
            item.click_down(self.m_card, value)




    def update_onRelease(self, gameTime):
        global movingFlag
        self.m_card.click_up(self.deck_list) # Handling card click up event



    def draw(self, surface):
        global output_string, end
        
        for item in self.deck_list:
            item.draw_card(surface, self.deck_dict) # Drawing each card on the surface

        timer() # Updating the timer
        self.m_card.draw(surface, self.deck_dict) # Drawing the moved card on the surface

        #Displays panel
        self.font.draw(surface, 'SCORE: ' + str(Cards.score), 480, 10)
        self.font.draw(surface, 'MOVES: ' + str(Cards.moves), 630, 10)
        self.font.draw(surface, output_string, 330, 10)
        self.button(surface, 255, 20, "Hint", 65, 40, color_dark, color_light, "Hint")
        # self.button(surface, 680, 500, "Pause", 100, 50, green, bright_green, "Pause")
        if self.check_complete():# Checking if the game is complete
            # Drawing the Solve button
            self.button(surface, 255, 70, "Solve", 65, 40, green, bright_green, "Solve")
        # If the game has ended
        if end:
            # Drawing the Quit button
            self.button(surface, 255, 70, "Quit", 65, 40, black, nblack, "Quit")
        

    def shuffle_cards(self):
        """This shuffle the cards,  Returning the shuffled list"""
        lst = list(self.deck_dict.keys())
        random.shuffle(lst)
        return lst

    #Function to draw buttons on the screen
    def button(self, surface, x, y, msg, w, h, ic, ac, action=None, width=2, border_radius=15):
        global count, cards_hid, end
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y: # Checking if the mouse is over the button
            pygame.draw.rect(surface, BLACK, [x, y, w, h], width, border_radius)
            pygame.draw.rect(surface, ac, (x, y, w, h), width, border_radius)
            if (click[0] == 1) and action is not None:
                if action == "Hint": # If the action is to show a hint
                    answ = self.pile_hints(surface)
                    if not answ:
                        answ = self.deck_hints(surface)
                        if answ:
                            end = False
                    else:
                        end = False


                    if len(self.deck_list[0].hidden_cards) == 0: # If there are no hidden cards
                        # print("Cards list",len(self.deck_list[0].cards_list))
                        if cards_hid != len(self.deck_list[0].cards_list):
                            pass
                        else:
                            if (not answ) and (not self.hints):
                                auto_change()

                if action == "Solve":
                    self.game.changeState(self.endState) # Changing the game state to endState

                if action == "Quit":
                    self.game.changeState(self.failState) # Changing the game state to failState
        else:
            pygame.draw.rect(surface, BLACK, [x, y, w, h], 0, border_radius )
            pygame.draw.rect(surface, ic, (x, y, w, h) , 0 , border_radius)

        self.font.draw(surface, msg, x + 5, y + 5)

    #Function to check hints from cards in the board and show them
    def pile_hints(self, surface):
        answer = False
        ace_hint = False
        king_hint = False

        for item in (x for x in self.deck_list if isinstance(x, Card1)): # Looping through Card1 instances. Means shown card in piles
            # print(item.cards[-1])
            t = item
            if len(item.cards) == 0:
                continue

            moving = item.cards[0] # Getting the first card that can be moved being moved from the pile
            # print("Moving", moving)

            if "ace" in moving: # If the moving card is an Ace
                ace_hint = True
                for i in (x for x in self.deck_list if isinstance(x, Card3)):
                    # print(i.hidden_cards)
                    if len(i.cards) == 0:
                        pygame.draw.rect(surface, red, [i.rect.left, i.rect.top, 71, 97], 6) # Drawing hint to win pile
                        pygame.draw.rect(surface, red, [t.rect.left, t.rect.top, 71, 97], 6) # Drawing ace rectangle
                        break
            elif "king" in moving and len(item.hidden) > 0: # If the moving card is a King and there are hidden cards
                for i in (x for x in self.deck_list if isinstance(x, Card1) and len(x.cards) == 0):
                    pygame.draw.rect(surface, red, [i.rect.left, i.rect.top, 71, 97], 6)
                    k = t.rect.top
                    king_hint = True
                    for zz in t.cards:
                        pygame.draw.rect(surface, red, [t.rect.left, k, 71, 97], 6) # Drawing king rectangle to new pile
                        k -= 16
                    else:
                        break

            else: # For other cards, >1 cards in pile that can be moved
                for item2 in (xx for xx in self.deck_list if isinstance(xx, Card1) and xx != item):
                    k = item2
                    if len(item2.cards) != 0:
                        answer = item.checkvalid(moving, item2.cards[-1])
                        if answer:
                            i = t.rect.top
                            for _ in t.cards:
                                pygame.draw.rect(surface, red, [t.rect.left, i, 71, 97], 6)
                                i -= 16
                            i = k.rect.top
                            for _ in k.cards:
                                pygame.draw.rect(surface, red, [k.rect.left, i, 71, 97], 6)
                            break
                else: # If no valid move was found, check if the card can be moved to a winning pile
                    moving = item.cards[-1]
                    for item3 in (xx for xx in self.deck_list if isinstance(xx, Card3)):
                        # print(item3.cards)
                        k = item3
                        if len(item3.cards) != 0: # If there are cards in the item
                            answer = item3.check_validpile(moving, item3.cards[-1]) # Checking if the card can be moved to the winning pile
                            if answer: # If a valid move is found
                                i = k.rect.top
                                pygame.draw.rect(surface, red, [k.rect.left, i, 71, 97], 6)# Drawing pile rectangle
                                i = item.rect.top
                                pygame.draw.rect(surface, red, [item.rect.left, i, 71, 97], 6) # Drawing card rectangle
                                break

            # Returning True to indicate a hint was found
            if ace_hint or answer or king_hint:
                return True
        else:
            return False # Returning False if no hints were found

    # Function to check hints from cards in the deck and show them on the screen.
    def deck_hints(self, surface):
        t = self.deck_list[0]
        kinn = 0
        #print("Card2 length",len(t.cards_list))
        #print("Hint", t.hintcounts)
        #print("Card2 hidden", t.hidden_cards)
        k = t.cards
        if len(k):
            op = t
            kk = t.cards[-1]
            # print(t.cards_list[0])
            if "ace" in kk:
                # print("Ace here")
                for i in (x for x in self.deck_list if isinstance(x, Card3)):
                    if len(i.cards) == 0:
                        pygame.draw.rect(surface, red, [op.rect.left, op.rect.top, 71, 97], 6)
                        pygame.draw.rect(surface, red, [i.rect.left, i.rect.top, 71, 97], 6)
                        return True
            elif "king" in kk:
                for uu in (x for x in self.deck_list if isinstance(x, Card1) and len(x.cards) == 0):
                    kinn = 1
                    aa = uu.rect.top
                    pygame.draw.rect(surface, red, [t.rect.left, t.rect.top, 71, 97], 6)
                    pygame.draw.rect(surface, red, [uu.rect.left, aa, 71, 97], 6)
                    return True
                if kinn == 0:
                    pygame.draw.rect(surface, red, [30, 30, 71, 97], 6)
                    return False
            else:

                for item2 in (xx for xx in self.deck_list if isinstance(xx, Card1)):
                    ppp = item2
                    if len(ppp.cards) != 0:
                        answer = item2.checkvalid(t.cards[-1], ppp.cards[-1])
                        if answer:
                            pygame.draw.rect(surface, red, [t.rect.left, t.rect.top, 71, 97], 6)
                            pygame.draw.rect(surface, red, [ppp.rect.left, ppp.rect.top, 71, 97], 6)
                            return True
                else:
                    mm = t
                    for item3 in (xx for xx in self.deck_list if isinstance(xx, Card3)):
                        # print(item3.cards)
                        pp = item3
                        if len(item3.cards) != 0:
                            answer = item3.check_validpile(mm.cards[-1], item3.cards[-1])
                            if answer:
                                oo = pp.rect.top
                                pygame.draw.rect(surface, red, [pp.rect.left, oo, 71, 97], 6)
                                oo = mm.rect.top
                                pygame.draw.rect(surface, red, [mm.rect.left, oo, 71, 97], 6)
                                return True
                    else:
                        pygame.draw.rect(surface, red, [30, 30, 71, 97], 6)
                        return False

        else:
            pygame.draw.rect(surface, red, [30, 30, 71, 97], 6)
            return False

    #Function to check if the game is complete testing all piles and deck
    def check_complete(self):
        for item1 in (xx for xx in self.deck_list if isinstance(xx, Card1) and len(xx.cards) != 0): # Looping through pile instances
            if len(item1.hidden) > 0 or (len(self.deck_list[0].hidden_cards) != 0 or len(
                    self.deck_list[0].cards_list) != 0): # Checking if there are hidden cards
                return False # Returning False to indicate the game is not complete
        else:
            return True # Returning True to indicate the game is complete

    # Function to check hints for cards in the deck. When button is pressed check if there is at least on hint to continue the game
    def available_hints(self, value):
        t = self.deck_list[0]
        #Track hint  answers
        answer = False
        ace_hint = False
        king_hint = False
        k = t.cards_list
        kinn = 0
        # print("Hidden",k)
        # print("Card",t.cards)
        # print("Card list", t.cards_list)
        numb = 3 if value == 1 else 1 # Setting the number of cards to show based on players choice
        #Displaying top 3 cards from start to last with the same order as the deck.
        numb = -numb
        ll = numb
        len = -1
        yy = ll
        zz = len
        top3 = k[:yy - 1:zz]
        zz = zz + 1

        while top3: # While there are cards in top3. Top3 means deck stacks when player choice is 3
            i = top3[-1]
            #Always check the top card in the top3.
            if "ace" in i:
                for ll in (x for x in self.deck_list if isinstance(x, Card3)):
                    # print("Found spot ace")
                    if not ll.cards:
                        ace_hint = True # Setting Ace hint flag to True
                        break
            elif "king" in i:
                for uu in (x for x in self.deck_list if isinstance(x, Card1)):
                    if not uu.cards:
                        # print("Found spot king")
                        kinn = 1
                        king_hint = True # Setting King hint flag to True
                        break
                if kinn == 0:
                    king_hint = False
            else:

                for item2 in (xx for xx in self.deck_list if isinstance(xx, Card1)):
                    ppp = item2
                    # print("PPP", ppp.cards)
                    # print("PPP", ppp.cards[-1])
                    if ppp.cards:
                        answer = item2.checkvalid(i, ppp.cards[-1]) # Checking if the move is valid
                        if answer:
                            break
                else:
                    for item3 in (xx for xx in self.deck_list if isinstance(xx, Card3)):
                        # print("Item3", item3.cards[-1])
                        # print("I in ", i)
                        if item3.cards:
                            answer = item3.check_validpile(i, item3.cards[-1])
                            if answer:
                                break
                        else:
                            answer = False

            if ace_hint or answer or king_hint:
                return True
            yy = yy + numb
            zz = zz + numb

            top3 = k[yy:zz:]
            counts = 0
            for _ in top3:
                counts += 1
            if counts > 0:
                top3[0], top3[-1] = top3[-1], top3[0]


        return False
