import mancala
import minimax

m = mancala.Mancala("Human", "CPU")
ai = minimax.MiniMax(mancala.PLAYER2, depth=5)

while not m.is_game_over():
    try:
        print(m)
        if m.current_player() == mancala.PLAYER1:
            move = int(input("current player: %s" % m.get_current_player_name()))
        else:
            print("getting move from AI")
            move = ai.get_next_move(m)
            print("AI chose %i" % move)
        m.play_turn(move)

    except Exception as e:
        print(e.message)

print(m.get_winner() + " wins!")