import mancala

m = mancala.Mancala("Alice", "Bob")

while not m.is_game_over():
    try:
        print(m)
        move = int(input("current player: %s" % m.get_current_player_name()))
        m.play_turn(move)

    except Exception as e:
        print(e.message)

print(m.get_winner() + " wins!")


