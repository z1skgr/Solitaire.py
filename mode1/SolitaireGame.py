import random
import pygame
import pyautogui
import time
import itertools

from pygame.mixer import SoundType

from mode1 import Cards
from mode1.Cards import *
from mode1.Raspigame import GameState
from mode1.Bitmapfont import *

black = (0, 0, 0)
nblack = (128, 128, 128)
white = (255, 255, 255)
red = (200, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)

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
globalhid = 0


def autochange():
    global end
    pyautogui.alert('No Moves Available')
    end = True


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


def initmusic():
    sound1 = pygame.mixer.Sound('cas music.wav')
    pygame.mixer.Channel(0).play(sound1)
    sound1.play(-1)


class PlayGameState(GameState):
    sound: SoundType

    def __init__(self, game, endState, failState):
        super(PlayGameState, self).__init__(game)
        self.deck_dict = {}
        self.deck_list = []
        self.restart = 0
        self.endState = endState
        self.failState = failState
        self.pile1 = 7
        self.pile2 = 4

        self.start_path = None
        self.final_path = None
        self.m_card = None
        self.card_list = []
        self.hints = None

        self.font = BitmapFont('fasttracker2-style_12x12.png', 12, 12)
        self.initialise()

    def initialise(self):
        global globalhid
        self.initialiseDeck()
        self.initialiseTable()
        globalhid = len(self.deck_list[0].hidden_cards)
        initmusic()

    def initialiseDeck(self):
        self.m_card = MovedCard()
        for s in ["spades", "clubs", "diamonds", "hearts"]:
            for i in range(1, 14):
                self.start_path = '../mode1/playing_cards'
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

    def initialiseTable(self):
        self.deck_list.append(Card2(130, 30))
        leng = len(self.deck_list)
        for i in range(leng, self.pile1 + 1):
            self.deck_list.append(Card1(30 + 100 * (i - 1), 160, i))
        for i in range(1, self.pile2 + 1):
            self.deck_list.append(Card3(330 + 100 * (i - 1), 30))

        for i in range(1, self.pile1 + 1):
            self.deck_list[i].extend_list(self.card_list[:i])
            del self.card_list[:i]

        self.deck_list[0].hidden_cards.extend(self.card_list)

    def update(self, gameTime):

        for item in self.deck_list:
            if isinstance(item, Card3):
                if len(item.cards) != 13:
                    return False
        else:
            self.game.changeState(self.endState)

    def newupdate(self, gameTime, value):
        global globalhid
        if len(self.deck_list[0].hidden_cards) == 0:
            self.hints = self.availablehints(value)

        if len(self.deck_list[0].cards_list) == 0:
            globalhid = len(self.deck_list[0].hidden_cards)

        # print("HInt", self.hints)

        for item in self.deck_list:
            item.click_down(self.m_card, value)

    def newnewupdate(self, gameTime):
        self.m_card.click_up(self.deck_list)

    def draw(self, surface):
        global output_string, end
        for item in self.deck_list:
            item.draw_card(surface, self.deck_dict)

        timer()
        self.m_card.draw(surface, self.deck_dict)
        self.font.draw(surface, 'SCORE: ' + str(Cards.score), 480, 10)
        self.font.draw(surface, 'MOVES: ' + str(Cards.moves), 630, 10)
        self.font.draw(surface, output_string, 330, 10)
        self.button(surface, 255, 20, "Hint", 65, 40, red, bright_red, "Hint")
        # self.button(surface, 680, 500, "Pause", 100, 50, green, bright_green, "Pause")
        if self.checkcomplete():
            self.button(surface, 255, 70, "Solve", 65, 40, green, bright_green, "Solve")

        if end:
            self.button(surface, 255, 70, "Quit", 65, 40, black, nblack, "Quit")

    def shuffle_cards(self):
        """This shuffle the cards"""
        lst = list(self.deck_dict.keys())
        random.shuffle(lst)
        return lst

    def button(self, surface, x, y, msg, w, h, ic, ac, action=None):
        global count, globalhid, end
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(surface, BLACK, [x, y, w, h], 3)
            pygame.draw.rect(surface, ac, (x, y, w, h))
            if (click[0] == 1) and action is not None:
                if action == "Hint":
                    # hintbutt = self.Hintfunction1(surface)
                    # if (hintbutt == False):
                    # print(self.hints)
                    answ = self.Hintfunction1(surface)
                    # print("Answ1",answ)
                    if not answ:
                        answ = self.Hintfunction2(surface)
                        if answ:
                            end = False
                        # print("Answ2", answ)
                    else:
                        end = False

                    # print("LEN",len(self.deck_list[0].hidden_cards))
                    # print("Hntcount",self.hintcount)

                    if len(self.deck_list[0].hidden_cards) == 0:
                        # print("Globalhid",globalhid)
                        # print("Len cardslist",len(self.deck_list[0].cards_list))
                        if globalhid != len(self.deck_list[0].cards_list):
                            pass
                        else:
                            if (not answ) and (not self.hints):
                                autochange()

                if action == "Solve":
                    self.game.changeState(self.endState)

                if action == "Quit":
                    self.game.changeState(self.failState)
        else:
            pygame.draw.rect(surface, BLACK, [x, y, w, h], 3)
            pygame.draw.rect(surface, ic, (x, y, w, h))

        self.font.draw(surface, msg, x + 5, y + 5)

    def Hintfunction1(self, surface):
        answer = False
        aceanswer = False
        kinganswer = False

        for item in (x for x in self.deck_list if isinstance(x, Card1)):
            # print(item.cards[-1])
            t = item
            # print(len(item.cards))
            if len(item.cards) == 0:
                continue

            moving = item.cards[0]
            # print("Moving", moving)

            if "ace" in moving:
                aceanswer = True
                for i in (x for x in self.deck_list if isinstance(x, Card3)):
                    # print(i.hidden_cards)
                    if len(i.cards) == 0:
                        pygame.draw.rect(surface, red, [i.rect.left, i.rect.top, 71, 97], 6)
                        pygame.draw.rect(surface, red, [t.rect.left, t.rect.top, 71, 97], 6)
                        break
            elif "king" in moving and len(item.hidden) > 0:
                for i in (x for x in self.deck_list if isinstance(x, Card1) and len(x.cards) == 0):
                    pygame.draw.rect(surface, red, [i.rect.left, i.rect.top, 71, 97], 6)
                    k = t.rect.top
                    kinganswer = True
                    for zz in t.cards:
                        pygame.draw.rect(surface, red, [t.rect.left, k, 71, 97], 6)
                        k -= 16
                    else:
                        break

            else:
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
                else:
                    moving = item.cards[-1]
                    for item3 in (xx for xx in self.deck_list if isinstance(xx, Card3)):
                        # print(item3.cards)
                        # print(item3.hidden_cards)
                        k = item3
                        if len(item3.cards) != 0:
                            answer = item3.checkvalidpile(moving, item3.cards[-1])
                            if answer:
                                i = k.rect.top
                                pygame.draw.rect(surface, red, [k.rect.left, i, 71, 97], 6)
                                i = item.rect.top
                                pygame.draw.rect(surface, red, [item.rect.left, i, 71, 97], 6)
                                break

            if aceanswer or answer or kinganswer:
                return True
        else:
            return False

    def Hintfunction2(self, surface):
        t = self.deck_list[0]
        kinn = 0
        # print("Card2 lem",len(t.cards_list))
        # print("Card2 Hidden len", len(t.hidden_cards))
        # print("HInt", t.hintcounts)
        # print("Card2 list", t.cards_list)
        # print("Card2 hidden", t.hidden_cards)
        # print("Card2 cards", t.cards)
        # print("Card2 len", len(t.cards))
        k = t.cards
        # print("k", k)
        if len(k):
            # print("Opened")
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
                    # print("MM", mm)
                    for item3 in (xx for xx in self.deck_list if isinstance(xx, Card3)):
                        # print(item3.cards)
                        pp = item3
                        if len(item3.cards) != 0:
                            answer = item3.checkvalidpile(mm.cards[-1], item3.cards[-1])
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
            # print("Closed")
            pygame.draw.rect(surface, red, [30, 30, 71, 97], 6)
            return False

    def checkcomplete(self):
        for item1 in (xx for xx in self.deck_list if isinstance(xx, Card1) and len(xx.cards) != 0):
            if len(item1.hidden) > 0 or (len(self.deck_list[0].hidden_cards) != 0 or len(
                    self.deck_list[0].cards_list) != 0):
                return False
        else:
            return True

    def availablehints(self, value):
        t = self.deck_list[0]
        answer = False
        aceanswer = False
        kinganswer = False
        k = t.cards_list
        # print(k)
        kinn = 0
        # print("Hidden",k)
        # print("Card",t.cards)
        # print("Card list", t.cards_list)
        numb = 3 if value == 1 else 1
        numb = -numb
        ll = numb
        len = -1
        # print(numb)
        yy = ll
        zz = len
        top3 = k[:yy - 1:zz]
        zz = zz + 1

        while top3:
            # print("TOp 3", top3)
            i = top3[-1]
            # print("I", i)
            if "ace" in i:
                # print("Ace king")
                for ll in (x for x in self.deck_list if isinstance(x, Card3)):
                    # print("Found spot ace")
                    if not ll.cards:
                        aceanswer = True
                        break
            elif "king" in i:
                # print("King here")
                for uu in (x for x in self.deck_list if isinstance(x, Card1)):
                    if not uu.cards:
                        # print("Found spot king")
                        kinn = 1
                        kinganswer = True
                        break
                if kinn == 0:
                    kinganswer = False
            else:

                for item2 in (xx for xx in self.deck_list if isinstance(xx, Card1)):
                    ppp = item2
                    # print("PPP", ppp.cards)
                    # print("PPP", ppp.cards[-1])
                    if ppp.cards:
                        answer = item2.checkvalid(i, ppp.cards[-1])
                        if answer:
                            break
                else:
                    # print("MM", mm)
                    for item3 in (xx for xx in self.deck_list if isinstance(xx, Card3)):
                        # print("Item3", item3.cards[-1])
                        # print("I in ", i)
                        if item3.cards:
                            answer = item3.checkvalidpile(i, item3.cards[-1])
                            # print("Answer3", answer)
                            if answer:
                                break
                        else:
                            answer = False

            if aceanswer or answer or kinganswer:
                return True
            yy = yy + numb
            # print("Yy", yy)
            zz = zz + numb
            # print("Zz", zz)
            top3 = k[yy:zz:]
            countss = 0
            for _ in top3:
                countss += 1
            if countss > 0:
                top3[0], top3[-1] = top3[-1], top3[0]

            # print("TOpp", top3)

        return False
