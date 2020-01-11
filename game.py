import pygame
from pygame.locals import *

from card import Card, DeckType, Suit, Value, ScoreSystem, Dealer

pygame.init()
screen = None
# noinspection PyShadowingNames
class CardSprite:
    RED_COLOR = (255, 0, 0)
    BLACK_COLOR = (0, 0, 0)
    CARD_COLOR = (255, 255, 255)
    HOVER_COLOR = (0, 255, 255)

    WHR = 7/5 #width-height ratio
    font = pygame.font.SysFont("Arial Unicode MS", 24)
    screen = globals()['screen']

    def __init__(self, card, size, color=CARD_COLOR, show=True, screen=screen, draw_border=True):
        self.card = card #this should be the Card object that it actually represents
        self._size = size
        self.show = show
        self.screen = screen
        self.color = color
        self.draw_border = True

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if len(size) == 4:
            if isinstance(size, tuple):
                self._size = list(size)
            else:
                self._size = size
        elif len(size) != 4:
            raise ValueError(f"Sprites must have a size with 4 parameters (width, height, x, y); got {size}")

    def draw(self):
        if self.show:
            pygame.draw.rect(screen, self.color, self._size)
            if self.is_hovered():
                pygame.draw.rect(screen, CardSprite.HOVER_COLOR, self._size, 1)
            elif self.draw_border:
                pygame.draw.rect(screen, CardSprite.BLACK_COLOR, self._size, 1)

            screen.blit(
                CardSprite.font.render(repr(self.card), self.x+self.width//4, CardSprite.RED_COLOR if self.card.is_red() else CardSprite.BLACK_COLOR),
                (self.x+self.width/4, self.y, self.width, self.height)
            )

    def __repr__(self):
        return f"Sprite: {self.card} @ {self._size}"

    def is_hovered(self): return self.x < pygame.mouse.get_pos()[0] < self.x + self.width and self.y < pygame.mouse.get_pos()[1] < self.y + self.height
    @property
    def x(self): return self._size[0]
    @x.setter
    def x(self, x): self._size[0] = x
    @property
    def y(self): return self._size[1]
    @y.setter
    def y(self, y): self._size[1] = y
    @property
    def width(self): return self._size[2]
    @width.setter
    def width(self, width): self._size[2] = width
    @property
    def height(self): return self._size[3]
    @height.setter
    def height(self, height): self._size[3] = height


dealer = Dealer(scoresystem=ScoreSystem(ScoreSystem.StandardScores.INTERNATIONAL))
deck, hands = dealer.deal(Dealer.make_deck(), players=4)

hand = [CardSprite(c, (0 + i*80, 0, 80, 80*CardSprite.WHR)) for i, c in enumerate(hands[0])]
print(hand)

def main(width=1400, height=500):
    global screen
    pygame.display.set_caption("Card Shark")
    screen = pygame.display.set_mode((width, height))

    running = True
    while running:
        screen.fill((0, 0, 0))
        for card in hand:
            card.draw()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                for card in hand:
                    if card.is_hovered():
                        played = hand.pop(hand.index(card))
                        print(played)

            if event.type == pygame.QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
        pygame.display.flip()




if __name__ == '__main__':
    main()
