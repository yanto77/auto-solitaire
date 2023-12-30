# import pyautogui as gui
import pickle
import heapq

from utils import timing
from screen_reader import ScreenReader
from state import State

@timing
def find_winning_moves(initial):
    print('Finding winning moves for ...\n{}'.format(initial))

    states = [initial]
    seen_states = set()
    idx = 0
    while states:
        s1 = heapq.heappop(states)
        for move in s1.get_moves():
            idx += 1
            s2 = s1.take_move(move)

            if s2 not in seen_states:
                if (idx % 10 == 0):
                    print("Evaluated {} steps, visited {}, unvisited {} .....".format(idx, len(seen_states), len(states)), end='\r')

                unfinished = sum(1 for i in range(9) if not s2.is_stack_finished(i))
                if unfinished == 1:
                    print("Evaluated {} steps, visited {}, unvisited {} .....\n".format(idx, len(seen_states), len(states)))
                    return s2.moves
                # else:
                #     input("Press Enter to continue...")
                #     print("\x1B[2J\x1B[H") # clear screen and move cursor to top-left corner

                seen_states.add(s2)
                heapq.heappush(states, s2)

    raise Exception("couldn't win the game :(")

if __name__ == "__main__":
    initial = ScreenReader.get_initial_state()
    with open('state.pickle', 'wb') as out_file:
        pickle.dump(initial, out_file)

    with open('state.pickle', 'rb') as in_file:
        initial = pickle.load(in_file)

    moves = find_winning_moves(initial)
    print(moves)

    # s1 = initial
    # for move in moves:
    #     s2 = s1.take_move(move)
    #     print('REPLAY')
    #     print('Pre:\n{}'.format(s1))
    #     print('Post:\n{}'.format(s2))

    #     input("Press Enter to continue...")
    #     print("\x1B[2J\x1B[H") # clear screen and move cursor to top-left corner
    #     s1 = s2
