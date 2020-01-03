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
        0:Suit.HEARTS, "H": Suit.HEARTS,
        1:Suit.CLUBS, "C": Suit.CLUBS,
        2:Suit.DIAMONDS, "D": Suit.DIAMONDS,
        3:Suit.SPADES, "S": Suit.SPADES,
        4:Suit.JOKER
    } #0-H, 1-C, 2-D, 3-S, 4-J

    #A smarter programmer (read: future me when I'm less tired) would overhaul the idx to incr by one and just use the same values
    value_map = {
        0:Value.ACE, "A":Value.ACE,
        1:Value.TWO, "2":Value.TWO,
        2:Value.THREE, "3":Value.THREE,
        3:Value.FOUR, "4":Value.FOUR,
        4:Value.FIVE, "5": Value.FIVE,
        5:Value.SIX, "6": Value.SIX,
        6:Value.SEVEN, "7": Value.SEVEN,
        7:Value.EIGHT, "8": Value.EIGHT,
        8:Value.NINE, "9": Value.NINE,
        9:Value.TEN, "T": Value.TEN,
        10:Value.JACK, "J": Value.JACK,
        11:Value.QUEEN, "Q": Value.QUEEN,
        12:Value.KING, "K": Value.KING,
        99: Value.JOKER, "$": Value.JOKER,
    } #0-A, 1-2, 2-3, 3-4, 4-5, 5-6, 6-7, 7-8, 8-9, 9-10, 10-J, 11-Q, 12-K, 99-J

    color_map = {
        "R":Color.RED, "B":Color.BLACK
    }

    group_map = {
        "#":{"type":"value", "set":{Value.TWO, Value.THREE, Value.FOUR, Value.FIVE, Value.SIX, Value.SEVEN, Value.EIGHT, Value.NINE,
              Value.TEN}},
        "F":{"type":"value", "set":{Value.JACK, Value.QUEEN, Value.KING}}
    }

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

            # compares.append([lambda card: float(score) if ((not value or card.value == value) and (not suit or card.suit == suit) and (not color or card.color == color)) else None])
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

deck, hands = Card.deal(Card.make_deck(), players=4)
s = ScoreSystem(ScoreSystem.StandardScores.HEARTS)
print(s.score(hands[0]))