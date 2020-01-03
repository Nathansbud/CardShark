from enum import Enum, auto
from random import shuffle

#######
#Cards (A-K)
#0-12: Hearts
#13-25: Clubs
#26-38: Diamonds
#39-51: Spades
#52, 53: Red Joker, Black Joker
#######
def ls(l): return [len(s) for s in l]

class Suit(Enum):
    HEARTS = auto()
    CLUBS = auto()
    DIAMONDS = auto()
    SPADES = auto()
    JOKER = auto()

class Value(Enum):
    JOKER = auto()
    ACE = auto()
    KING = auto()
    QUEEN = auto()
    JACK = auto()
    TEN = auto()
    NINE = auto()
    EIGHT = auto()
    SEVEN = auto()
    SIX = auto()
    FIVE = auto()
    FOUR = auto()
    THREE = auto()
    TWO = auto()

class Color(Enum):
    RED = auto()
    BLACK = auto()

class Card:
    suit_map = {
        0:Suit.HEARTS,
        1:Suit.CLUBS,
        2:Suit.DIAMONDS,
        3:Suit.SPADES,
        4:Suit.JOKER
    } #0-H, 1-C, 2-D, 3-S, 4-J
    value_map = {
        0:Value.ACE,
        1:Value.TWO,
        2:Value.THREE,
        3:Value.FOUR,
        4:Value.FIVE,
        5:Value.SIX,
        6:Value.SEVEN,
        7:Value.EIGHT,
        8:Value.NINE,
        9:Value.TEN,
        10:Value.JACK,
        11:Value.QUEEN,
        12:Value.KING,
        99: Value.JOKER,
    } #0-A, 1-2, 2-3, 3-4, 4-5, 5-6, 6-7, 7-8, 8-9, 9-10, 10-J, 11-Q, 12-K, 99-J

    def __init__(self, idx):
        self.idx = idx
        self.suit = Card.suit_map[idx // 13] #52, 53 = Joker
        self.value = Card.value_map[idx % 13 if idx < 52 else 99]
        self.color = Color.RED if self.suit is Suit.DIAMONDS or self.suit is Suit.HEARTS or idx == 52 else Color.BLACK

    def __repr__(self):
        if self.value is not Value.JOKER:
            value = str(self.value).split(".")[1].lower().capitalize()
            suit = str(self.suit).split(".")[1].lower().capitalize()
            return f"{value} of {suit}"
        else:
            color = str(self.color).split(".")[1].lower().capitalize()
            return f"{color} Joker"

    @staticmethod
    def make_deck(decks=1, with_jokers=False, shuffled=True):
        cards = [Card(i) for i in range(54 if with_jokers else 52)]*decks
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
            for i in range(len(d) % amount):
                h[i].append(d[-i])

        d = d[sum([len(l) for l in h]):] #Deck is whatever is remaining
        return d, h

deck, hands = Card.deal(Card.make_deck(), players=10)
print(ls(hands))

class ScoreSystem:
    """
    Codes:
        - 1, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A, $: Card Codes
        - R, B: Color Codes (Red, Black)
        - H, S, C, D: Suit Codes (Heart, Spades, Clubs, Diamonds)
        - X, #, F: Set Codes (All, Numbers, Face Cards)
    """
    def __init__(self, ruleset="X-0"):
        self.rules = ScoreSystem.parse_ruleset(ruleset)

    @staticmethod
    def parse_ruleset(ruleset):
        rules = ruleset.split(",").reverse()
        #these rules should be parsed into a list of expressions in the form:
        #lambda card: if card.suit/value/color == COMPARE_VALUE: return score,
        # i.e.
        # if c.value == Value.QUEEN and c.suit == Suit.SPADES:
        #   return 13
        #
        return []

    def score(self, card_set):
        score = 0
        for c in card_set:
            for rule in self.rules:
                score += rule(c)



        return score

s = ScoreSystem()
print(s.score([Card(50)]))