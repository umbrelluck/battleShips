"""
for debugging
"""
import time, sets, sys, random

info = [1, 2, 3]


class Game:
    def __init__(self):
        ans = input("Are you going to play with Computer or Friend? [C/f]\n => ")
        if ans in ["c", "C", ""]:
            computer = True
        else:
            computer = False
        self.current_pl = random.randint(0, 1)

        if computer:
            name = input("Choose your name or press <Enter>: ")
            if name == "":
                name = "Player 1"
            you = sets.Human(name)
            ans = input("Do you want auto generation of the field? [Y/n]\n => ")
            if ans in ["Y", "y", ""]:
                you_field = sets.Field(True)
            else:
                you_field = sets.Field(False)
            en = sets.PC(sets.Field(True))
            en_field = sets.Field(True)
            en.add_field(you_field)
            you.add_field(en_field)
            self.players = [you, en]
            self.pc = True
        else:
            name = input("Choose your name or press <Enter>: ")
            if name == "":
                name = "Player 1"
            pl1 = sets.Human(name)
            ans = input("Do you want auto generation of the field? [Y/n]\n => ")
            if ans in ["Y", "y", ""]:
                pl1_field = sets.Field(True)
            else:
                pl1_field = sets.Field(False)
            input("Now your oponent`s turn <Press any key to continue> ")
            name = input("Choose your name or press <Enter>: ")
            if name == "":
                name = "Player 2"
            pl2 = sets.Human(name)
            ans = input("Do you want auto generation of the field? [Y/n]\n => ")
            if ans in ["Y", "y", ""]:
                pl2_field = sets.Field(True)
            else:
                pl2_field = sets.Field(False)
            self.pc = False
            pl2.add_field(pl1_field)
            pl1.add_field(pl2_field)
            self.players = [pl1, pl2]

    def prnt(self, info, end=False):
        if end:
            for i in range(-1, 10):
                tmp = str(info[i]) if info != [1, 2, 3] and i in [0, 1, 2] else ""
                print(self.players[1].field.field_with_ships(i) + self.players[
                    0].field.field_with_ships(i, end="             ") + tmp)
        else:
            if self.pc:
                for i in range(-1, 10):
                    tmp = str(info[i]) if info != [1, 2, 3] and i in [0, 1, 2] else ""
                    print(self.players[1].field.field_with_ships(i) + self.players[
                        0].field.field_without_ships(i, end="             ") + tmp)
            else:
                for i in range(-1, 10):
                    tmp = str(info[i]) if info != [1, 2, 3] and i in [0, 1, 2] else ""
                    print(self.players[1].field.field_without_ships(i, end="             ") +
                          self.players[0].field.field_without_ships(i) + tmp)

    def play(self):
        global info
        print("\nIt is {}`s move now\n".format(self.players[self.current_pl].name))
        self.prnt(info)
        # if self.pc:
        #     time.sleep(1.25)
        flag, pos = self.players[self.current_pl].read_shot_position()
        info[0] = pos
        info[1] = self.players[(self.current_pl + 1) % 2].name + "`s ships: " + str(
            self.players[self.current_pl].field.shp)
        info[2] = self.players[self.current_pl].name + "`s ships: " + str(
            self.players[(self.current_pl + 1) % 2].field.shp)
        while flag:
            # victory
            info[2] = self.players[(self.current_pl + 1) % 2].name + "`s ships: " + str(
                self.players[self.current_pl].field.shp)
            info[1] = self.players[self.current_pl].name + "`s ships: " + str(
                self.players[(self.current_pl + 1) % 2].field.shp)
            if self.players[self.current_pl].field.count == 0:
                print("\n{} WINS!\n".format(self.players[self.current_pl].name))
                self.prnt(info, True)
                print("{} WINS!".format(self.players[self.current_pl].name))
                # input("Press any key to exit...")
                # sys.exit()
                return True
            print("\nIt is {}`s move now\n".format(self.players[self.current_pl].name))
            self.prnt(info)
            flag, pos = self.players[self.current_pl].read_shot_position()
            info[0] = pos
            info[1] = self.players[(self.current_pl + 1) % 2].name + "`s ships: " + str(
                self.players[self.current_pl].field.shp)
            info[2] = self.players[self.current_pl].name + "`s ships: " + str(
                self.players[(self.current_pl + 1) % 2].field.shp)
        self.current_pl = (self.current_pl + 1) % 2
        return False


if __name__ == "__main__":
    game = Game()
    while True:
        if game.play():
            break
