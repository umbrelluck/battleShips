import random

to_remove = []


class Ship:
    def __init__(self, length, pos=(0, 0)):
        self.bow = pos
        if length[1] >= length[0]:
            self.horizontal = True
        else:
            self.horizontal = False
        self._length = length
        self._hit = [False] * max(length)
        self.icon = u'\u2588'

    def shoot_at(self, pos):
        if (pos[0] in range(self.bow[0], self.bow[0] + self._length[0])) and (
                pos[1] in range(self.bow[1], self.bow[1] + self._length[1])):
            if self.horizontal:
                self._hit[abs(pos[1] - self.bow[1])] = True
            else:
                self._hit[abs(pos[0] - self.bow[0])] = True
            return self._hit.count(True) == len(self._hit)

    def prnt(self, i, j):
        position = max(abs(self.bow[0] - i), abs(self.bow[1] - j))
        if self._hit[position]:
            return u'\u256c'
        else:
            return u'\u2588'
        # return self.icon


class Field:
    def __init__(self, auto=False):
        self.count = 10
        self._ships = [[None] * 10 for i in range(10)]
        if auto:
            for leng in [4, 3, 2, 1]:
                self._place(leng)
        else:
            for i in range(10):
                wh = input("Top left coor od ship (like a8): ")
                wh = (int(wh[1]) - 1, ord(wh[0].lower()) - 97)
                ln = list(map(int, input("How to place (like 1,4): ").split(",")))
                self.place(wh, ln)
        self.shp = {4: 1, 3: 2, 2: 3, 1: 4}

    def find_free(self):
        res = []
        for i in range(len(self._ships)):
            for j in range(len(self._ships[i])):
                if not self._ships[i][j]:
                    res.append((i, j))
        return res

    def _free(self, pos, length):
        for i in range(length[0]):
            for j in range(length[1]):
                try:
                    if type(self._ships[pos[0] + i][pos[1] + j]) in [Ship, int]:
                        raise IndexError
                except IndexError:
                    return False
        return True

    def place(self, pos, length):
        ship = Ship(length, pos)
        if self._free(pos, length):
            for i in range(-1, length[0] + 1):
                for j in range(-1, length[1] + 1):
                    try:
                        self._ships[abs(pos[0] + i)][abs(pos[1] + j)] = -1
                    except IndexError:
                        continue
            for i in range(length[0]):
                for j in range(length[1]):
                    self._ships[pos[0] + i][pos[1] + j] = ship
            return True
        else:
            return False

    def _place(self, length):
        for i in range(5 - length):
            free, avail = self.find_free(), [(1, length), (length, 1)]
            leng = random.choice(avail)
            avail.remove(leng)
            while True:
                if len(free) == 0:
                    free = self.find_free()
                    # try
                    leng = avail[0]
                pos = random.choice(free)
                free.remove(pos)
                if self.place(pos, leng):
                    break

    def shoot_at(self, pos):
        global to_remove
        to_remove = []
        if type(self._ships[pos[0]][pos[1]]) == Ship:
            if self._ships[pos[0]][pos[1]].shoot_at(pos):
                bow, length = self._ships[pos[0]][pos[1]].bow, self._ships[pos[0]][pos[1]]._length
                self.update(bow, length, to_remove)
                self.count -= 1
            return True
        else:
            self._ships[pos[0]][pos[1]] = u'\xa4'
            return False

    def update(self, pos, length, to_remove):
        for i in range(-1, length[0] + 1):
            for j in range(-1, length[1] + 1):
                try:
                    self._ships[abs(pos[0] + i)][abs(pos[1] + j)] = u'\xa4'
                    to_remove.append((abs(pos[0] + i), abs(pos[1] + j)))
                except IndexError:
                    continue
        for i in range(length[0]):
            for j in range(length[1]):
                self._ships[pos[0] + i][pos[1] + j] = u'\u256c'
        a = len(range(-1, length[0] + 1)) - 2
        b = len(range(-1, length[1] + 1)) - 2
        self.shp[a * b] -= 1

    def field_with_ships(self, i, end="             "):
        if i in [-1, 10]:
            return "   |{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|    ".format(
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j") + end
        # for i in range(len(self._ships)):
        res = "{:>2} ".format(i + 1)
        for j in range(len(self._ships[i])):
            if type(self._ships[i][j]) in [type(None), int]:
                res += "|   "
            elif type(self._ships[i][j]) == Ship:
                res += "| " + "{:^1}".format(self._ships[i][j].prnt(i, j)) + " "
            else:
                tmp = self._ships[i][j]
                res += "| " + "{:^1}".format(self._ships[i][j]) + " "
        res += "| " + "{:<2} ".format(i + 1) + end
        return res

    def field_without_ships(self, i, end="\n"):
        if i in [-1, 10]:
            return "   |{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|    ".format(
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j") + end
        # for i in range(len(self._ships)):
        res = "{:>2} ".format(i + 1)
        for j in range(len(self._ships[i])):
            if type(self._ships[i][j]) in [type(None), int]:
                res += "|   "
            elif type(self._ships[i][j]) == Ship:
                if self._ships[i][j].prnt(i, j) == u'\u256c':
                    res += "| " + "{:^1}".format(u'\u256c') + " "
                else:
                    res += "| " + " " + " "
            else:
                tmp = self._ships[i][j]
                res += "| " + "{:^1}".format(self._ships[i][j]) + " "
        res += "| " + "{:<2} ".format(i + 1) + end
        return res


class Player:
    def __init__(self, name):
        self.name = name
        self.field = None
        self.hited = []

    def add_field(self, fld):
        """"
        first field - your field
        """
        self.field = fld

    def shoot_at(self, pos):
        return self.field.shoot_at(pos)

    def read_shot_position(self):
        ans = input("\nWhere to shoot (a8 for example) --> ")
        ans = ans[-1] + ans[:-1] if ans[0] in "0123456789" else ans
        while ans in self.hited or int(ans[1:]) not in range(1, 11) or ans[0] \
                not in "abcdefghij" or ans == "":
            ans = input("Where to shoot (a8 for example) --> ")
            ans = ans[-1] + ans[:-1] if ans[0] in "0123456789" else ans
        self.hited.append(ans)
        pos = int(ans[1:]) - 1, ord(ans[0].lower()) - 97
        flag = self.shoot_at(pos)
        global to_remove
        if flag and len(to_remove) > 0:
            for elem in to_remove:
                self.hited.append(chr(elem[1] + 97) + str(elem[0] + 1))
            # to_remove = []
        return flag, self.name + "`s move: " + chr(pos[1] + 97) + str(pos[0] + 1)


class Human(Player):
    pass


class PC(Player):
    position_moves = {(1, 0): [], (-1, 0): [], (0, 1): [], (0, -1): []}
    cur_pos = ()
    base_pos = ()
    bt_pos = ()
    prnt_pos = []
    to_think = False

    def __init__(self, field, name="PC"):
        global to_remove
        to_remove = []
        super().__init__(name)
        self.field = field
        self.to_hit = [(i, j) for i in range(10) for j in range(10)]
        self.update_restore(to_remove)

    def update_restore(self, to_remove):
        for elem in to_remove:
            try:
                self.to_hit.remove(elem)
            except ValueError:
                continue
        self.cur_pos = ()
        self.base_pos = ()
        self.position_moves = {(1, 0): [], (-1, 0): [], (0, 1): [], (0, -1): []}
        self.to_think = False

    def read_shot_position(self):
        self.prnt_pos = []
        if self.cur_pos == ():
            pos = random.choice(self.to_hit)
            self.bt_pos = pos[:]
        else:
            pos = self.cur_pos
        try:
            self.to_hit.remove(pos)
            flag = self.shoot_at(pos)
            if len(self.base_pos) != 0:
                self.position_moves[self.base_pos].append(flag)
            # print("Normal shoot at {} with {}".format(pos, flag))
        except Exception:
            self.position_moves[self.base_pos].append(False)
            flag = self.think()
            pos = self.cur_pos
            self.to_think = False
        global to_remove
        if flag == -1:
            flag = True
        elif flag:
            self.to_think = True
        if flag and len(to_remove) > 0:
            self.update_restore(to_remove)
            self.to_think = False
        if self.to_think:
            flag = self.think()
        tmp = " ".join(chr(elem[1] + 97) + str(elem[0] + 1) for elem in self.prnt_pos)
        try:
            return flag, self.name + "`s move: " + chr(pos[1] + 97) + str(pos[0] + 1) + " " + tmp
        except Exception:
            return flag, self.name + "`s move: " + tmp

    def think(self):
        # print(self.position_moves)
        if self.cur_pos in ((), -1):
            self.cur_pos = self.bt_pos[:]
        # else:
        #     self.cur_pos = self.cur_pos[0] + self.base_pos[0], self.cur_pos[1] + \
        #                    self.base_pos[1]
        avail = [elem for elem in self.position_moves if self.position_moves[elem] == []]
        while self.cur_pos not in self.to_hit:
            # print("why are you changing?")
            if len(avail) == 0:
                self.cur_pos = ()
                self.base_pos = ()
                self.to_think = False
                return -1
            if self.base_pos != () and (self.position_moves[self.base_pos] != []
                                        and self.position_moves[self.base_pos][-1]):
                self.position_moves[self.base_pos].append(False)
            else:
                self.base_pos = ()
                self.cur_pos = self.bt_pos[:]
                self.base_pos = random.choice(avail)
                avail.remove(self.base_pos)
            self.cur_pos = (self.base_pos[0] + self.cur_pos[0], self.base_pos[1] + self.cur_pos[1])
        # print(self.position_moves)
        self.prnt_pos.append(self.cur_pos)
        self.to_hit.remove(self.cur_pos)
        hit = self.field.shoot_at(self.cur_pos)
        # print(
        #     "Shooting at {} is {} with start {} and base {}".format(self.cur_pos, hit,
        #     self.bt_pos,
        #                                                             self.base_pos))
        self.position_moves[self.base_pos].append(hit)
        if hit:
            self.cur_pos = self.cur_pos[0] + self.base_pos[0], self.cur_pos[1] + \
                           self.base_pos[1]
        elif len(self.position_moves[self.base_pos]) > 1:
            self.base_pos = -self.base_pos[0], -self.base_pos[1]
            self.cur_pos = self.base_pos[0] + self.bt_pos[0], self.base_pos[1] + self.bt_pos[1]
        else:
            self.cur_pos = -1
        global to_remove
        if len(to_remove) > 0:
            self.update_restore(to_remove)
        return hit


if __name__ == "__main__":
    you = Player("Yarko")
    you_field = Field(True)
    en = Player("PC")
    en_field = Field(True)
    you.add_field((you_field, en_field))

    field = Field(True)
    for i in range(-1, 10):
        print(field.field_with_ships(i) + field.field_without_ships(i))
    field.shoot_at((0, 0))
    field.shoot_at((3, 3))
    field.shoot_at((4, 4))
    field.shoot_at((5, 5))
    field.shoot_at((9, 9))
    for i in range(-1, 10):
        print(field.field_with_ships(i) + field.field_without_ships(i))
