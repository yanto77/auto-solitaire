
import pyscreeze
from os import listdir
from os.path import isfile, join

from utils import timing
from state import State

# [ num = 6-10 or 12, suite = 0-3 ]
# NB: for numbered cards, we don't need to distinguish between suites of same color.
CARD_TYPES = { 
    'img/ace1.png': (12, 0),
    'img/ace2.png': (12, 1),
    'img/ace3.png': (12, 2),
    'img/ace4.png': (12, 3),
    'img/black6.png': (6, 0),
    'img/black7.png': (7, 0),
    'img/black8.png': (8, 0),
    'img/black9.png': (9, 0),
    'img/black10.png': (10, 0),
    'img/red6.png': (6, 2),
    'img/red7.png': (7, 2),
    'img/red8.png': (8, 2),
    'img/red9.png': (9, 2),
    'img/red10.png': (10, 2),
}

FILEPATH = 'img/'

class ScreenReader():
    @staticmethod
    @timing
    def get_screen():
        # Take a screenshot
        # screen = pyscreeze.screenshot() # TODO
        screen = pyscreeze._load_cv2('foo.png', grayscale=False)
        return screen

    @staticmethod
    @timing
    def find_cards(screen):
        cards = []
        for fname in listdir(FILEPATH):
            fpath = join(FILEPATH, fname)
            if not isfile(fpath):
                continue

            try:
                for box in pyscreeze.locateAll(fpath, screen, grayscale=False):
                    cards.append([fpath, box])
            except pyscreeze.ImageNotFoundException:
                continue

        if len(cards) != 36:
            raise Exception("Couldn't find all cards.")

        return cards

    @staticmethod
    def get_initial_state():
        screen = ScreenReader.get_screen()
        cards = ScreenReader.find_cards(screen)

        # Convert card pixel positions to stack indices
        min_x = min([box.left for (path, box) in cards])
        min_y = min([box.top for (path, box) in cards])
        for i in range(len(cards)):
            cards[i][1] = cards[i][1]._replace(
                left = int((cards[i][1].left - min_x) / 130),
                top = int((cards[i][1].top - min_y) / 30))
            cards[i][0] = CARD_TYPES[cards[i][0]]

        cards.sort(key = lambda x: (x[1].left, x[1].top))
        return State(cards)
