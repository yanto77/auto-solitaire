import pyautogui as gui
import pickle
import heapq
import time

from utils import timing
from screen_reader import ScreenReader, SCREEN_DX, SCREEN_DY
from state import State

# pyautogui makes moves instant with 0.10, so use value slightly above it, 
# as otherwise the game doesn't recognize the input
ANIMATION_TIME = 0.11

@timing
def find_winning_moves(initial):
    states = [initial]
    seen_states = set()
    idx = 0
    while states:
        s1 = heapq.heappop(states)
        for move in s1.get_moves():
            idx += 1
            s2 = s1.take_move(move)

            if s2 not in seen_states:
                unfinished = sum(1 for i in range(9) if not s2.is_stack_finished(i))
                if unfinished == 1:

                    print("> Found winning moves. Steps: {}. Visited: {}. Frontier: {}.".format(idx, len(seen_states), len(states)))
                    return s2.moves
                # else:
                #     input("Press Enter to continue...")
                #     print("\x1B[2J\x1B[H") # clear screen and move cursor to top-left corner

                seen_states.add(s2)
                heapq.heappush(states, s2)

    raise Exception("couldn't win the game :(")

@timing
def play_single_game():
    initial = ScreenReader.get_initial_state()

    # Use caching to speed up debugging
    # with open('state.pickle', 'wb') as out_file:
    #     pickle.dump(initial, out_file)
    # with open('state.pickle', 'rb') as in_file:
    #     initial = pickle.load(in_file)

    moves = find_winning_moves(initial)
    s1 = initial
    
    (top_y, top_x) = s1.top_left
    (spare_y, spare_x) = (top_y - SCREEN_DY * 6, top_x + SCREEN_DX * 8)

    gui.moveTo(top_x, top_y, ANIMATION_TIME, gui.easeInOutQuad)

    for move in moves:
        s2 = s1.take_move(move)

        (from_idx, to_idx, count) = move
        from_count = len(s1.stacks[from_idx]) - count
        to_count = len(s1.stacks[to_idx])

        from_y = top_y + (from_count * SCREEN_DY) + 10
        from_x = top_x + (from_idx * SCREEN_DX) + 60
        to_y = top_y + (to_count * SCREEN_DY) + 10
        to_x = top_x + (to_idx * SCREEN_DX) + 60

        if to_idx == 9:
            to_y = spare_y
            to_x = spare_x
        elif from_idx == 9:
            from_y = spare_y
            from_x = spare_x
    
        gui.moveTo(from_x, from_y, ANIMATION_TIME, gui.easeInOutQuad)
        gui.dragTo(to_x, to_y, ANIMATION_TIME, gui.easeInOutQuad)

        # input("Press Enter to continue...")
        # print("\x1B[2J\x1B[H") # clear screen and move cursor to top-left corner
        s1 = s2

    # Wait for congratulating message
    time.sleep(2) 

    # Click on "NEW GAME". NB: gui.click() doesn't work here, maybe it's too quick.
    (new_y, new_x) = (top_y + SCREEN_DY * 14.5, top_x + SCREEN_DX * 7)
    gui.moveTo(new_x, new_y, ANIMATION_TIME, gui.easeInOutQuad)
    gui.drag(20, 0, ANIMATION_TIME, gui.easeInOutQuad)

    # Wait for new cards
    time.sleep(6) 

if __name__ == "__main__":
    while True:
        play_single_game()
