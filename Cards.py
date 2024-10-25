import pygame
# Define the colors:
# ----------------------

AQUA = (0, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
OLIVE = (128, 128, 0)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)

# -----------------------
score: int = 0
moves: int = 0
size = 128, 128


class MovedCard(object):
    """This class represents the cards that will move on the screen"""

    def __init__(self):

        self.moved = False  # This variable is True when there is a card moving on
        # the screen.
        self.moved_card = []  # This variable will contain the name of the card.
        self.card_d = ()
        self.cards = None  # This is object
        self.pile = 0

    def click_up(self, deck_list):
        global score, moves
        """This is used when the user release the mouse button."""
        if len(self.moved_card) > 0:
            for item in deck_list:
                if not isinstance(item, Card2):
                    if item.check_pos() and item.check_card(self.moved_card): # Check position and card validity
                        # Score points based on the type of pile the card is moved to. +5 to winning pile or move from board pile to board pile
                        if isinstance(item, Card3):
                            score += 5
                            moves += 1
                        else:
                            if self.pile != item.numpile:
                                score += 5
                                moves += 1
                        item.add_card(self.moved_card)
                        self.moved = False # Reset moved status
                        self.moved_card = [] # Clear the moved card list

                        if isinstance(self.cards, Card1): # Success move means new card is shown from the pile
                            self.cards.show_card() # Show the card

                        self.cards = None
                        break
            else:
                #Reset moved status and moved card list if the card is not moved to a valid pile
                self.cards.add_card(self.moved_card)
                self.moved = False
                self.moved_card = []
                self.cards = None

    def draw(self, screen, card_dict):
        """This draw the moved cards onto the screen"""
        if self.moved: # Check if a card is currently moved
            #Draw moving card onto the screen
            pos = pygame.mouse.get_pos()
            x = pos[0] - self.card_d[0] # Calculate x position for drawing
            y = pos[1] - self.card_d[1] # Calculate y position for drawing
            # If more than one card is moved, show them on top of each other
            for item in self.moved_card:
                screen.blit(card_dict[item], [x, y])
                y += 16


class Card(object):
    def __init__(self, x, y):
        self.cards = []
        self.rect = pygame.Rect(x, y, 71, 97)

    def check_pos(self):
        """This check if the cursor is on the card"""
        pos = pygame.mouse.get_pos()
        if self.rect.left <= pos[0] <= self.rect.right:
            if self.rect.top <= pos[1] <= self.rect.bottom:
                return True # Return True if the cursor is on the card
            else:
                return False
        else:
            return False


class Card1(Card):
    def __init__(self, x, y, i):
        # call parent's constructor:
        Card.__init__(self, x, y)
        self.y = y
        self.hidden = []
        self.numpile = i
        global score

    #Function to extend new cards to a pile, reveal the top hidden card
    def extend_list(self, lst):
        self.hidden.extend(lst)
        self.cards.append(self.hidden.pop()) #Reveal new card
        if len(self.hidden) > 0:
            for i in range(len(self.hidden)):
                self.rect.top += 16

    #Function to draw hidden and cards on the board
    def draw_card(self, screen, card_dict):
        """This will draw all the cards on the screen"""
        pygame.draw.rect(screen, BLACK, [self.rect.left, self.rect.top, 71, 97], 1)
        i = self.y
        if len(self.hidden) > 0:
            for _ in self.hidden:
                # Hidden card layout
                backImg = pygame.image.load('backsmall.png')
                #Draw image of the back of the card
                screen.blit(backImg, [self.rect.left, i])
                # Outline
                pygame.draw.rect(screen, BLACK, [self.rect.left, i, 71, 97], 1)
                i += 16
        # Card layout for the visible card
        if len(self.cards) > 0:
            for item in self.cards:
                screen.blit(card_dict[item], [self.rect.left, i])
                i += 16

    #Function to add cards to a pile and calculate the position of the cards on the piles
    def add_card(self, card):
        if len(self.cards) > 0 or len(self.hidden) > 0: #Check if there are cards to add
            for i in range(len(card)): # Iterate through the cards to add
                self.rect.top += 16 # Move the card down by 16 pixels
        else: # Add cards to the new pile and draw them
            for i in range(len(card)):
                if i > 0:
                    self.rect.top += 16
        self.cards.extend(card)

    #Function on clicking the mouse button
    def click_down(self, card, value):
        """This is used when the user press the mouse button"""
        # Check if there are cards to click
        if len(self.cards) > 0:

            top = self.rect.top
            lst = []

            for i in range(len(self.cards)): # Iterate through the cards
                if self.check_pos(): # Check if the cursor is on the card
                    pos = pygame.mouse.get_pos()
                    lst.insert(0, self.cards.pop())
                    card.card_d = (pos[0] - self.rect.left, pos[1] -
                                   self.rect.top)  # Remove the card from the pile and make it movable
                    card.moved = True
                    card.cards = self
                    card.moved_card.extend(lst) # Add the clicked cards to the moved card list
                    card.pile = self.numpile # Set the pile number
                    if len(self.cards) > 0 or len(self.hidden) > 0:
                        self.rect.top -= 16 # Move the card up by 16 pixels
                    break
                else:
                    lst.insert(0, self.cards.pop()) # Remove the card and add it to the clicked list. Back to its place
                    self.rect.top -= 16
            else:
                self.rect.top = top
                self.cards.extend(lst)

    #Function to show a hidden card if there are no visible cards and hidden cards exist
    def show_card(self): # Check if there are no visible cards and hidden cards exist
        if len(self.cards) == 0 and len(self.hidden) > 0:
            self.cards.append(self.hidden.pop()) # Move a hidden card to the visible cards

    #Function to check if the moved card is valid
    def check_card(self, moved_card):
        # Get the first moved card
        card = moved_card[0]
        result = False
        if len(self.cards) == 0:
            if "king" in card: # Check if the moved card is a king
                result = True
        else:
            if "hearts" in card or "diamonds" in card:
                if "spades" in self.cards[-1] or "clubs" in self.cards[-1]:
                    next_card = "X"
                    if "king" in self.cards[-1]:
                        next_card = "queen"
                    elif "queen" in self.cards[-1]:
                        next_card = "jack"
                    elif "jack" in self.cards[-1]:
                        next_card = "10_"
                    elif "10_" in self.cards[-1]:
                        next_card = "9_"
                    elif "9_" in self.cards[-1]:
                        next_card = "8_"
                    elif "8_" in self.cards[-1]:
                        next_card = "7_"
                    elif "7_" in self.cards[-1]:
                        next_card = "6_"
                    elif "6_" in self.cards[-1]:
                        next_card = "5_"
                    elif "5_" in self.cards[-1]:
                        next_card = "4_"
                    elif "4_" in self.cards[-1]:
                        next_card = "3_"
                    elif "3_" in self.cards[-1]:
                        next_card = "2_"
                    elif "2_" in self.cards[-1]:
                        next_card = "ace"

                    if next_card in card:
                        result = True
            elif "hearts" in self.cards[-1] or "diamonds" in self.cards[-1]:
                next_card = "X"
                if "king" in self.cards[-1]:
                    next_card = "queen"
                elif "queen" in self.cards[-1]:
                    next_card = "jack"
                elif "jack" in self.cards[-1]:
                    next_card = "10_"
                elif "10_" in self.cards[-1]:
                    next_card = "9_"
                elif "9_" in self.cards[-1]:
                    next_card = "8_"
                elif "8_" in self.cards[-1]:
                    next_card = "7_"
                elif "7_" in self.cards[-1]:
                    next_card = "6_"
                elif "6_" in self.cards[-1]:
                    next_card = "5_"
                elif "5_" in self.cards[-1]:
                    next_card = "4_"
                elif "4_" in self.cards[-1]:
                    next_card = "3_"
                elif "3_" in self.cards[-1]:
                    next_card = "2_"
                elif "2_" in self.cards[-1]:
                    next_card = "ace"

                if next_card in card:
                    result = True

        return result

    #Function to instantiate solitaire rules for deck cards
    def checkvalid(self, mcard, mmcard):
        #Check pngs and take ths suit and the value of the cards
        v1 = mcard.find('_')  # Value and suit of the moving card
        v2 = mmcard.find('_') # Value and suit of the card to compare
        v_card1 = ""
        v_card2 = ""
        s_card1 = ""
        s_card2 = ""
        #
        for i in range(len(mcard)):
            if mcard[i] == '_':
                continue
            if i < v1:
                v_card1 += mcard[i]
            else:
                s_card1 += mcard[i]
        for i in range(0, len(mmcard)):
            if mmcard[i] == '_':
                continue
            if i < v2:
                v_card2 += mmcard[i]
            else:
                s_card2 += mmcard[i]

        #Converts the card values to numeric values:
        if "jack" in v_card1:
            n_card1 = 11
        elif "queen" in v_card1:
            n_card1 = 12
        elif "king" in v_card1:
            n_card1 = 13
        elif "ace" in v_card1:
            n_card1 = 1
        else:
            n_card1 = int(v_card1)

        if "jack" in v_card2:
            n_card2 = 11
        elif "queen" in v_card2:
            n_card2 = 12
        elif "king" in v_card2:
            n_card2 = 13
        elif "ace" in v_card2:
            n_card2 = 1
        else:
            n_card2 = int(v_card2)

        #Checks if the move is valid based on Solitaire rules:
        if "hearts" in s_card1 or "diamonds" in s_card1:
            if "spades" in s_card2 or "clubs" in s_card2:
                if n_card2 == n_card1 + 1:
                    return True
                else:
                    return False
            else:
                return False
        else:
            if "hearts" in s_card2 or "diamonds" in s_card2:
                if n_card2 == n_card1 + 1:
                    return True
                else:
                    return False
            else:
                return False


class Card2(Card):
    def __init__(self, x, y):
        # call parent's constructor:
        Card.__init__(self, x, y)
        self.hidden_cards = []
        self.cards_list = []
        self.x = x

    #Function to draw cards from the deck list
    def draw_card(self, screen, card_dict):

        """This will draw all the cards on the screen"""
        x = self.x
        if len(self.hidden_cards) > 0:
            # Back of the card
            backImg = pygame.image.load('backsmall.png')
            screen.blit(backImg, [30, 30])

            #
            pygame.draw.rect(screen, BLACK, [30, 30, 71, 97], 2)
            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20
        else:
            if len(self.cards_list) > 0 and len(self.cards) > 0:
                for item in self.cards:
                    screen.blit(card_dict[item], [x, self.rect.top])
                    x += 20
            pygame.draw.ellipse(screen, OLIVE, [40, 40, 60, 60], 5)

    # Function to handling clicks on the deck list
    def click_down(self, card, value):
        global moves
        """This is used when the user press the mouse button"""
        # Check if the cursor is on the card and there are cards
        if self.check_pos() and len(self.cards) > 0:
            pos = pygame.mouse.get_pos()
            c = self.cards.pop()
            card.moved_card.append(c)# Add the card to the moved card list
            self.cards_list.remove(c) # Remove the card from the cards list
            card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top) # Store the card's position
            card.moved = True
            card.cards = self
            self.rect.left -= 20
        else:
            # Check if the mouse is within the bounds to open cards from the deck list
            pos = pygame.mouse.get_pos() # Get the current mouse position
            flag = False
            if 30 <= pos[0] <= 101:
                if 30 <= pos[1] <= 127:
                    flag = True
            if flag:
                moves += 1
                self.rect.left = self.x
                if len(self.hidden_cards) > 0:
                    self.cards = []
                    for i in range(1 if value == 0 else 3): # Determine how many cards to draw
                        c = self.hidden_cards.pop() # Remove a hidden card
                        self.cards_list.insert(0, c) # Add it to the cards list
                        self.cards.append(c) # Add it to the cards
                        if len(self.hidden_cards) == 0 and i < 2: # Check if there are no more hidden cards
                            break

                else:
                    #Reroll card in the deck from the beginning
                    self.hidden_cards.extend(self.cards_list)
                    self.cards_list = []
                    self.cards = []

                if len(self.cards) > 1:
                    for i in range(len(self.cards)):
                        if i > 0:
                            self.rect.left += 20
    # Function to add cards to the deck list, and handling dimensions
    def add_card(self, card):
        self.cards.extend(card)
        self.cards_list.extend(card)
        self.rect.left += 20


class Card3(Card):
    def __init__(self, x, y):
        # call parent's constructor:
        Card.__init__(self, x, y)
        self.cards_list = []
        self.x = x
        self.lock = True

    # Function to draw cards from the winning pile
    def draw_card(self, screen, card_dict):

        """This will draw all the cards on the screen"""
        pygame.draw.rect(screen, WHITE, [self.rect.left, self.rect.top, 71, 97], 1)
        if len(self.cards) > 0:
            screen.blit(card_dict[self.cards[-1]], [self.rect.left, self.rect.top])

    # Function to check if the card is valid for the winning pile
    def check_card(self, moved_card):
        result = False
        if len(moved_card) == 1:
            card = moved_card[0]
            if len(self.cards) == 0:
                if card[:3] == 'ace':
                    result = True
            else:
                suit = self.cards[0][4:]
                next_card = ''
                if suit in card:
                    if 'ace' in self.cards[-1]:
                        next_card = '2_' + suit
                    elif '2_' in self.cards[-1]:
                        next_card = '3_' + suit
                    elif '3_' in self.cards[-1]:
                        next_card = '4_' + suit
                    elif '4_' in self.cards[-1]:
                        next_card = '5_' + suit
                    elif '5_' in self.cards[-1]:
                        next_card = '6_' + suit
                    elif '6_' in self.cards[-1]:
                        next_card = '7_' + suit
                    elif '7_' in self.cards[-1]:
                        next_card = '8_' + suit
                    elif '8_' in self.cards[-1]:
                        next_card = '9_' + suit
                    elif '9_' in self.cards[-1]:
                        next_card = '10_' + suit
                    elif '10_' in self.cards[-1]:
                        next_card = 'jack_' + suit
                    elif 'jack_' in self.cards[-1]:
                        next_card = 'queen_' + suit
                    elif 'queen_' in self.cards[-1]:
                        next_card = 'king_' + suit

                    if next_card == card:
                        result = True
        return result

    def click_down(self, card, value):
        if not self.lock:
            """This is used when the user press the mouse button"""
            if self.check_pos() and len(self.cards) > 0:
                pos = pygame.mouse.get_pos()
                card.moved_card.append(self.cards.pop())
                card.card_d = (pos[0] - self.rect.left, pos[1] - self.rect.top)
                card.moved = True
                card.cards = self

    def add_card(self, card):
        self.cards.extend(card)

    # Function to instantiate solitaire rules for winning pile cards
    def check_validpile(self, mcard, mmcard):
        val_1 = mcard.find('_')
        val_2 = mmcard.find('_')
        v_card1 = ""
        v_card2 = ""
        s_card1 = ""
        s_card2 = ""

        for i in range(len(mcard)):
            if mcard[i] == '_':
                continue
            if i < val_1:
                v_card1 += mcard[i]
            else:
                s_card1 += mcard[i]
        for i in range(0, len(mmcard)):
            if mmcard[i] == '_':
                continue
            if i < val_2:
                v_card2 += mmcard[i]
            else:
                s_card2 += mmcard[i]

        if "jack" in v_card1:
            n_card1 = 11
        elif "queen" in v_card1:
            n_card1 = 12
        elif "king" in v_card1:
            n_card1 = 13
        elif "ace" in v_card1:
            n_card1 = 1
        else:
            n_card1 = int(v_card1)

        if "jack" in v_card2:
            n_card2 = 11
        elif "queen" in v_card2:
            n_card2 = 12
        elif "king" in v_card2:
            n_card2 = 13
        elif "ace" in v_card2:
            n_card2 = 1
        else:
            n_card2 = int(v_card2)

        if s_card1 == s_card2:
            if n_card1 == n_card2 + 1:
                return True
            else:

                return False
        else:
            return False
