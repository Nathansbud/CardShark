from enum import Enum, auto
from random import shuffle



class DeckType(Enum):
    STANDARD = 52
    STANDARD_JOKERS = 54

    def __init__(self, count):
        self.count = count

class Suit(Enum):
    HEARTS = (0, "Hearts", "H", "♥")
    CLUBS = (1, "Clubs", "C", "♣")
    DIAMONDS = (2, "Diamonds", "D", "♦")
    SPADES = (3, "Spades", "S", "♠")
    JOKER = (4, "Joker", "JO", "$")

    def __init__(self, idx, full, code, symbol):
        self.idx = idx
        self.full = full
        self.code = code
        self.symbol = symbol

class Value(Enum):
    ACE = (0, "Ace", "A", "A")
    TWO = (1, "Two", "2", "2")
    THREE = (2, "Three", "3", "3")
    FOUR = (3, "Four", "4", "4")
    FIVE = (4, "Five", "5", "5")
    SIX = (5, "Six", "6", "6")
    SEVEN = (6, "Seven", "7", "7")
    EIGHT = (7, "Eight", "8", "8")
    NINE = (8, "Nine", "9", "9")
    TEN = (9, "Ten", "10", "T")
    JACK = (10, "Jack", "J", "J")
    QUEEN = (11, "Queen", "Q", "Q")
    KING = (12, "King", "K", "K")
    JOKER = (99, "Joker", "JO", "$")

    def __init__(self, idx, full, rep, code):
        self.idx = idx
        self.full = full
        self.rep = rep
        self.code = code

class Color(Enum):
    RED = ("Red", "R")
    BLACK = ("Black", "B")

    def __init__(self, full, rep):
        self.full = full
        self.rep = rep

class Card:
    minify = True

    suit_map = {
        k:s
        for s in Suit
        for k in [s.idx, s.code]
    }
    value_map = {
        k:v
        for v in Value
        for k in [v.idx, v.code]
    }
    color_map = {c.rep:c for c in Color}
    group_map = {
        "#":{"type":"value", "set":{Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX, Value.SEVEN, Value.EIGHT, Value.NINE,
              Value.TEN}}, #{v for v in Value if 0 < v.idx < 10}
        "F":{"type":"value", "set":{Value.JACK, Value.QUEEN, Value.KING}} #{v for v in Value if 0 < v.idx < 10}
    }

    def __init__(self, idx):
        self.idx = idx
        self.value = Card.value_map[idx % 13 if idx < 52 else 99]
        self.suit = Card.suit_map[idx // 13] #52, 53 = Joker
        self.color = Color.RED if self.suit is Suit.DIAMONDS or self.suit is Suit.HEARTS or idx == 52 else Color.BLACK

    def is_red(self):
        return self.color == Color.RED

    def __repr__(self):
        if Card.minify:
            if self.value is not Value.JOKER: return f"{self.value.rep}{self.suit.symbol}"
            else: return f"{self.value.rep}{self.color.rep}"
        else:
            if self.value is not Value.JOKER: return f"{self.value.full} of {self.suit.full}"
            else: return f"{self.color.full} {self.value.full}"

class ScoreSystem:
    class StandardScores:
        HEARTS = "X-0,H-1,QS-13"
        INTERNATIONAL = "#-5,F-10,A-15,2-25"

    """
    Codes:
        - 1, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A, $: Card Codes
        - R, B: Color Codes (Red, Black)
        - H, S, C, D: Suit Codes (Heart, Spades, Clubs, Diamonds)
        - X, #, F: Set Codes (All, Numbers, Face Cards)
    """
    #Because of the way matching works, an "invalid" (non-match) code = "everything matches"...should prob change this but it means X-0 = non-match 0 points
    def __init__(self, ruleset): #Ruleset is inverted, later rules are evaluated first (i.e. HF-15,J-10, Jack of Hearts would match for 10)
        self.ruleset = ScoreSystem.parse_ruleset(ruleset)

    # noinspection PyShadowingNames
    @staticmethod
    def parse_ruleset(ruleset):
        rules = [r.strip() for r in ruleset.split(",")[::-1]] #Flip ruleset, priority is inverted
        compares = []
        for rule in rules:
            features, score = rule.split("-")
            feature_set = [f for f in features]
            suit, value, color, special = None, None, None, None
            for feature in feature_set:
                if feature in Card.value_map: value = Card.value_map[feature]
                elif feature in Card.suit_map: suit = Card.suit_map[feature]
                elif feature in Card.color_map: color = Card.color_map[feature]
                elif feature in Card.group_map: special = Card.group_map[feature]
            compares.append({"score":float(score), "value":value, "suit":suit, "color":color, "special":special})
        return compares

    def score(self, card_set):
        score = 0
        for card in card_set:
            for rule in self.ruleset:
                #this is a mess that needs cleaning
                if (not rule['value'] or card.value == rule['value']) and (not rule['suit'] or card.suit == rule['suit']) and (not rule['color'] or card.color == rule['color']):
                    if rule['special'] and \
                        ((rule['special']['type'] == 'value' and card.value in rule['special']['set']) or
                         (rule['special']['type'] == 'suit' and card.suit in rule['special']['set']) or
                         (rule['special']['type'] == 'color' and card.color in rule['special']['set'])):
                        print(card, rule['score'], "(Special)")
                        score += rule['score']
                        break
                    elif not rule['special']:
                        print(card, rule['score'], "(Normal)")
                        score += rule['score']
                        break
            else:
                print("No rules matched!")
        return score

class Dealer:
    def __init__(self, deck_type=DeckType.STANDARD, decks=1, scoresystem=None):
        self.deck_type = deck_type
        self.scoresystem = scoresystem
        self.deck = Dealer.make_deck(dt=deck_type, decks=decks)
        pass

    @staticmethod
    def make_deck(dt=DeckType.STANDARD, decks=1, shuffled=True):
        cards = [Card(i) for i in range(dt.count)] * decks
        if shuffled: shuffle(cards)
        return cards

    @staticmethod
    def deal(d, amt=-1, players=1):
        h = []
        if amt < 0:
            amount = len(d) // players
        else:
            amount = amt

        for i in range(players):
            h.append(d[amount * i:amount * (i + 1)])

        if amt < 0:
            # If a full deck deal, add the excess to each hand
            for i in range(1, len(d) % amount + 1):
                h[i].append(d[-i])

        d = d[sum([len(l) for l in h]):]  # Deck is whatever is remaining
        return d, h




