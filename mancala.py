import random

PLAYER1: int = 0
PLAYER2: int = 1
PLAYER1_BANK: int = 6
PLAYER2_BANK: int = 13


class Mancala:

    def __init__(self, player1_name='Player1', player2_name='Player2'):
        random.seed()

        # starting setup
        self._pits = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        #self._pits = [2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 0]
        self._round = 1
        self._players = [player1_name, player2_name]

        # current_player denotes whose turn it is
        self._starting_player = random.randint(PLAYER1, PLAYER2)
        self._current_player = self._starting_player
        self._game_over = False

    def get_player_pits(self, player: int):
        if player is None or (player != PLAYER1 and player != PLAYER2):
            e = Exception()
            e.message("Player must be either mancala.PLAYER1 or mancala.PLAYER2")
            raise e
        return {
                'pits': self._pits[0+player*7:6+player*7],
                'bank': self._pits[6+player*7]
            }

    def get_board_status(self):
        pass

    def __str__(self):

        p1s = self._players[PLAYER1]
        p2s = self._players[PLAYER2]

        list_for_str = list(map(lambda x: ' ' + str(x) if len(str(x)) == 1 else str(x), self._pits))
        list_for_str = list(reversed(list_for_str[0:6])) \
                       + [p1s + " " * max(0, 6-len(p1s))] \
                       + list_for_str[PLAYER1_BANK:(PLAYER1_BANK + 1)] \
                       + list_for_str[PLAYER2_BANK:(PLAYER2_BANK + 1)] \
                       + [p2s + " " * max(0, 12 - len(p2s))] \
                       + list_for_str[7:13]
        return '''
             5     4     3     2     1    0
      ---------------------------------------------
      |   | %s  |  %s | %s  | %s  | %s  | %s  |   |
%s| %s|-----------------------------------|%s |%s
      |   | %s  |  %s | %s  | %s  | %s  | %s  |   |
      ---------------------------------------------
            0      1     2     3     4     5
        ''' % tuple(list_for_str)

    def current_player(self):
        return self._current_player

    def play_turn(self, pit_number: int):
        if self._game_over:
            raise IllegalMoveError("Game is over")

        extra_turn = False

        if pit_number not in range(0, 6):
            raise InvalidError()

        if self.is_empty(pit_number):
            raise IllegalMoveError("Cannot play empty pit")

        pos = pit_number + self._current_player * 7
        hand = self._pits[pos]
        self._pits[pos] = 0
        pos = (pos + 1) % 14

        for i in range(hand, 0, -1):
            if self.on_opponents_bank(pos):
                pos = (pos + 1) % 14

            if i == 1:
                if self.on_own_bank(pos, self._current_player):
                    # advance the player turn token

                    extra_turn = True

                elif self.in_own_area(pos) and self._pits[pos] == 0:
                    opp_pit = self.get_opposite_pit(pos)
                    # bank the seeds in the opposite pit
                    self._pits[self.get_current_player_bank()] += (self._pits[opp_pit]+1)
                    self._pits[opp_pit] = 0

                    break

            self._pits[pos] += 1
            pos = (pos + 1) % 14

        # end game if all current player's pits are empty
        print("checking endgame status: "+str(self.get_player_pits(self._current_player)['pits']))
        if sum(self.get_player_pits(self._current_player)['pits']) == 0:
            self.end_game()

        elif not extra_turn:
            self._current_player = (self._current_player + 1) % 2

    def on_opponents_bank(self, pit_number: int) -> bool:
        return (self._current_player == PLAYER1 and pit_number == PLAYER2_BANK) \
               or \
               (self._current_player == PLAYER2 and pit_number == PLAYER1_BANK)

    def get_player_name(self, player_number: int):
        return self._players[player_number]

    def get_score(self, player=PLAYER1):

        if player == PLAYER1:
            return self._pits[PLAYER1_BANK]
        else:
            return self._pits[PLAYER2_BANK]

    def get_winner(self):
        if self._game_over:
            if self.get_score(PLAYER1) > self.get_score(PLAYER2):
                return self._players[PLAYER1]
            elif self.get_score(PLAYER1) == self.get_score(PLAYER2):
                return "TIE"
            return self._players[PLAYER2]
        else:
            return None

    def pits(self):
        return self._pits

    def is_empty(self, pit: int) -> bool:
        return self._pits[pit+self._current_player*7] == 0

    @staticmethod
    def player_owner(pit_number: int):
        if pit_number in range(0, 6):
            return PLAYER1
        elif pit_number in range(7, 13):
            return PLAYER2

        raise InvalidError()

    def get_current_player_bank(self):
        return PLAYER1_BANK+7*self._current_player

    @staticmethod
    def get_opposite_pit(pos: int) -> int:
        return 12 - pos

    def get_current_player_name(self):
        return self._players[self._current_player]

    def in_own_area(self, pos: int) -> bool:
        start_pos = 0+self._current_player*7
        return pos in range(start_pos, start_pos+6)

    @staticmethod
    def on_own_bank(pos: int, player: int) -> bool:
        return pos == 6 + 7*player

    def _is_game_over(self):
        return sum(self._pits[0:6]) == 0 or sum(self._pits[7:13]) == 0

    def end_game(self):
        self._pits[PLAYER1_BANK] += sum(self.get_player_pits(PLAYER1)['pits'])
        for i in range(6):
            self._pits[i] = 0

        self._pits[PLAYER2_BANK] += sum(self.get_player_pits(PLAYER2)['pits'])
        for i in range(7, 13):
            self._pits[i] = 0

        self._game_over = True

    def is_game_over(self):
        return self._game_over


class PositionError(Exception):
    """Player attempts a move not in their pit"""

    def __init__(self, player: str, pit_number: int):
        self.message = "Player %s cannot access pit %i" % (player, pit_number)


class InvalidError(Exception):
    """Attempt to access invalid pit id"""

    def __init__(self):
        self.message = "Attempted to access an invalid pit"


class IllegalMoveError(Exception):
    """performing an illegal move, such as selecting an empty pit"""
    def __init__(self, msg: str):
        self.message = msg


if __name__ == '__main__':
    m = Mancala()
    print(m._players)
    print("starting player is: %s" % m._players[m._current_player])
    print(m)
