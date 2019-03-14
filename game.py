from game_cont import Game

if __name__ == "__main__":
    while True:
        game = Game()
        while True:
            if game.play():
                break
        ans = input("Would you like to play one more time? [Y/n]\n => ")
        if ans not in ["Y", "y", '']:
            break
