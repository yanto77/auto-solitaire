import copy 

SUITES = ['♠', '♣', '♦', '♥']
COLORS = ['\033[38m', '\033[38m', '\033[31m', '\033[31m']

class State():
    def __init__(self, cards):
        self.moves = []
        self.stacks = []
        for i in range(9 + 1): # 9 stack, 1 spare
            self.stacks.append([])

        for (card, box) in cards:
            self.stacks[box.left].append(card)

    def __str__(self):
        out = ''
        for stack_idx in range(10):
            if (self.is_stack_finished(stack_idx)):
                out += '\033[95m{}: \033[0m'.format(stack_idx)
            else:
                out += '{}: '.format(stack_idx)

            for (num, suite) in self.stacks[stack_idx]:
                out += '{}{}{}{}, '.format(COLORS[suite], num, SUITES[suite], '\033[0m')

            if self.moves:
                (from_idx, to_idx, num) = self.moves[-1]
                if stack_idx == from_idx:
                    out += '\033[1m\033[33m --> ({}) \033[0m'.format(num)
                if stack_idx == to_idx:
                    out += '\033[1m\033[33m <-- ({}) \033[0m'.format(num)
            out += '\033[0m\n'

        if self.moves:
            out += str(self.moves[-1])

        return out
    
    def __hash__(self):
        return hash(tuple(tuple(s) for s in self.stacks))

    # NB: set() doesn't believe __hash__() alone, it will double-check with __eq__() ... 
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.stacks == other.stacks
        return NotImplemented

    def __lt__(self, other):
        unfinished1 = sum(1 for i in range(9) if not self.is_stack_finished(i))
        unfinished2 = sum(1 for i in range(9) if not other.is_stack_finished(i))
        return unfinished1 < unfinished2

    def __valid_sequence(self, bottom, top):
        (bn, bs), (tn, ts) = (bottom, top)
        if (bn == tn + 1) and (bs != ts):
            return True
        elif (bn == 12) and (tn == 12) and (bs == ts):
            return True

        return False

    def is_stack_finished(self, index):
        stack = self.stacks[index]
        if len(stack) == 4:
            ((n1, s1), (n2, s2), (n3, s3), (n4, s4)) = stack
            if n1 == n2 == n3 == n4 == 12 and s1 == s2 == s3 == s4:
                return True

        elif len(stack) == 5:
            ((n1, s1), (n2, s2), (n3, s3), (n4, s4), (n5, s5)) = stack
            if (n1 == 10) and (n2 == 9) and (n3 == 8) and (n4 == 7) and (n5 == 6):
                if (s1 != s2) and (s2 != s3) and (s3 != s4) and (s4 != s5):
                    return True

        return False

    def get_moves(self):
        result = [] # list of (from_idx, to_idx, count) tuples

        unfinished_stacks = set(i for i in range(9) if not self.is_stack_finished(i))

        # Move single card to spare place
        for src_idx in unfinished_stacks:
            if not self.stacks[9]:
                result.append((src_idx, 9, 1))

        # Move single card from spare place
        if self.stacks[9]:
            src_card = self.stacks[9][0]
            for dst_idx in unfinished_stacks:
                if self.stacks[dst_idx]:
                    dst_card = self.stacks[dst_idx][-1]
                    if (self.__valid_sequence(dst_card, src_card)):
                        result.append((9, dst_idx, 1))
                else:
                    result.append((9, dst_idx, 1))

        # Move multiple cards to another stack
        for src_idx in unfinished_stacks:
            stack = self.stacks[src_idx]
            if len(stack) == 0:
                continue

            # Get number of cards that can be moved away from this stack
            for card_idx in range(len(stack) - 1, -1, -1):
                if card_idx != 0 and self.__valid_sequence(stack[card_idx-1], stack[card_idx]):
                    continue
                else:
                    break
            move_count = len(stack) - card_idx
            src_card = stack[card_idx]

            # Check if these cards can be moved to destination stack.
            for dst_idx in unfinished_stacks:
                if src_idx == dst_idx:
                    continue
                
                if self.stacks[dst_idx]:
                    dst_card = self.stacks[dst_idx][-1]
                    if (self.__valid_sequence(dst_card, src_card)):
                        result.append((src_idx, dst_idx, move_count))
                else:
                    result.append((src_idx, dst_idx, move_count))

        return result

    def take_move(self, move):
        (src_idx, dst_idx, move_count) = move
        s2 = copy.deepcopy(self)
        cards = s2.stacks[src_idx][-move_count:]
        s2.stacks[src_idx][-move_count:] = []
        s2.stacks[dst_idx].extend(cards)
        s2.moves.append(move)
        return s2
