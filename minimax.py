import mancala as mc

SEP = '  '


class MiniMax:
    # m - reference to instance of active Mancala game, used for obtaining status
    # p - player number (0 for first player, 1 for second)

    def __init__(self, p: int, depth=3):
        self.p = p
        self._depth = depth

    def get_next_move(self, m: mc.Mancala) -> int:

        state = m.get_board_status()

        # state[mc.PLAYER1_BANK] = 0
        # state[mc.PLAYER2_BANK] = 0

        test_m = mc.Mancala()

        test_m.set_board_status(self.p, state)

        best_score = -100
        best_move = -1

        moves = test_m.get_valid_moves()
        for i in moves:
            # check the minimax value of each valid move
            # print("top level: move %i" % i)
            test_m.set_board_status(self.p, state)
            test_m.play_turn(i)
            test_score = self.minimax(test_m, self._depth)
            # best_score, best_move = max((best_score, best_move), (test_score, i),  key=lambda x: x[0])
            if test_score > best_score:
                best_score = test_score
                best_move = i
            print("top level: move %i, score %i" % (i, test_score))

        return best_move

    def get_next_maximizing_player(self, current_player: int) -> bool:
        return current_player == self.p

    def minimax(self, m: mc.Mancala, depth, turns_list = None):

        maximizing_player = (m.current_player() == self.p)

        if depth == 0 or m.is_game_over():
            # print("%s end node: %i" % ((SEP*self._depth),m.get_score(self.p) - m.get_score(1-self.p)))
            delta = m.get_score(self.p) - m.get_score(1 - self.p)
            return delta

        init_state = m.get_board_status()
        current_player = m.current_player()

        best_score = -100 if maximizing_player else 100

        for i in m.get_valid_moves():
            # print("%s P%i move: %i" % (SEP * (self._depth - depth), m.current_player(), i))
            m.play_turn(i)
            # if maximizing_player and m.current_player() == self.p:
            #    print("%s additional turn" % (SEP*(self._depth-depth)))

            node_weight = self.minimax(m, depth-1)
            best_score = max(best_score, node_weight) if maximizing_player else min(best_score, node_weight)
            m.set_board_status(current_player, init_state)

        return best_score
