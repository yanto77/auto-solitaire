from os import listdir
from os.path import isfile, join

import pyautogui as gui
import pyscreeze
import pickle

def get_initial_state():
    results = []

    screen = pyscreeze.screenshot()
    FILEPATH = 'img/'

    for fname in listdir(FILEPATH):
        fpath = join(FILEPATH, fname)
        if not isfile(fpath):
            continue

        try:
            for box in pyscreeze.locateAll(fpath, screen):
                results.append((fpath, box))
        except pyscreeze.ImageNotFoundException:
            continue

    if len(results) != 36:
        raise Exception("Couldn't find all cards.")

    return results


# state = get_initial_state()
# with open('state.pickle', 'wb') as out_file:
#     pickle.dump(state, out_file)

with open('state.pickle', 'rb') as in_file:
    state = pickle.load(in_file)

state = list(state)

# Convert to indices
min_x = min([box.left for (path, box) in state])
min_y = min([box.top for (path, box) in state])
for i in range(len(state)):
    state[i][1] = state[i][1]._replace(
        left = int((state[i][1].left - min_x) / 130),
        top = int((state[i][1].top - min_y) / 30))

state.sort(key = lambda x: (x[1].left, x[1].top))

for (path, box) in state:
    path = path.replace('img/', '').replace('.png', '')
    print(box.left, box.top, path)


# TODO:
# - doesn't recognize specific ace
# - mixes between red/black 10
# -> try 30x30 images ?