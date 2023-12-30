
import pyscreeze
from os import listdir
from os.path import isfile, join
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

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

MAX_WORKERS = 8

SCREEN_DX = 130
SCREEN_DY = 30

class ScreenReader():
    @staticmethod
    @timing
    def get_screen():
        # Take a screenshot
        screen = pyscreeze.screenshot()
        # screen = pyscreeze._load_cv2('foo.png', grayscale=False)
        return screen

    @staticmethod
    def locateSingle(screen, fpath):
        try:
            results = []
            for box in pyscreeze.locateAll(fpath, screen, grayscale=False):
                results.append([fpath, box])
            return results
        except pyscreeze.ImageNotFoundException:
            return None

    @staticmethod
    @timing
    def find_cards(screen):
        files = []
        FILEPATH = 'img/'
        for fname in listdir(FILEPATH):
            fpath = join(FILEPATH, fname)
            if isfile(fpath):
                files.append(fpath)

        cards = []
        with ThreadPoolExecutor(MAX_WORKERS) as pool:
            result = pool.map(ScreenReader.locateSingle, repeat(screen), files)
            for res in result:
                if res is not None:
                    cards.extend(res)

        if len(cards) != 36:
            raise Exception("Couldn't find all cards. Found: {}.".format(len(cards)))

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
                left = int((cards[i][1].left - min_x) / SCREEN_DX),
                top = int((cards[i][1].top - min_y) / SCREEN_DY))
            cards[i][0] = CARD_TYPES[cards[i][0]]

        cards.sort(key = lambda x: (x[1].left, x[1].top))
        return State(cards, (min_y, min_x))
