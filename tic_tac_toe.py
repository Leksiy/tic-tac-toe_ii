import random


class Options:
    def __init__(self):
        self.gamers = [0, 0]
        self.score = [0, 0]
        self.move_turn_start = 0


class Gamer:
    def __init__(self, char):
        self.CHAR = char
        self.GAMER_DICT = {1: 'Человек', 2: 'ИИ'}

        print('Игрок ', self.CHAR)
        for i in self.GAMER_DICT:
            print(str(i) + '. ' + self.GAMER_DICT[i])
        self.gamer_class = int(input())

    def __str__(self):
        return self.GAMER_DICT[self.gamer_class]

    def move(self, field, ai, gamer_id):
        i = 0
        j = 0
        if self.gamer_class == 1:
            move_legal = False
            while not move_legal:
                i, j = map(int, input('№ строки № столбца\n').split())
                move_legal = field.move_legal(i, j)
        else:
            i, j = ai.move(field, gamer_id + 1)
        return i, j

    def ii_train(self, result):
        if self.gamer_class == 2 and self.II_TRAIN:
            self.CPU.ii_train(result)


class AI:
    def __init__(self, neural_net):
        self.neural_net = neural_net
        self.moves = []
        self.cells_legal_list = []
        self.x = []
        self.y = []

    def move(self, field, gamer):
        self.cells_legal_list = field.cells_legal()
        self.x = field.cells_to_x(gamer)
        self.y = []
        print(self.neural_net.print_w())
        for i in self.cells_legal_list:
            x_all = self.x.copy()
            for j in i:
                match j:
                    case 0:
                        x_all.extend((1, 0, 0))
                    case 1:
                        x_all.extend((0, 1, 0))
                    case 2:
                        x_all.extend((0, 0, 1))
            y = self.neural_net.activate(x_all)
            print(x_all, y)
            self.y.append(y)
        cells_ai_list = []
        for i in range(len(self.y)):
            if self.y[i] == 1:
                cells_ai_list.append(self.cells_legal_list[i])
        if len(cells_ai_list) > 0:
            cell = random.choice(cells_ai_list)
        else:
            cell = random.choice(self.cells_legal_list)
        print(self.y, cells_ai_list, cell)
        self.moves.append([self.x, cell, 1 if cell in cells_ai_list else -1])
        print(self.moves)
        return cell


class Field:
    def __init__(self):
        self.N = 3
        self.CHAR = [' ', 'X', 'O']

        self.field = [[0 for j in range(self.N)] for i in range(self.N)]

    def __str__(self):
        field = '  0  1  2\n'
        for i in range(self.N):
            field += str(i) + ' '
            for j in range(self.N):
                field += ' ' + self.CHAR[self.field[i][j]] + ' '
            field += '\n'
        return field

    def clear(self):
        self.field = [[0 for j in range(self.N)] for i in range(self.N)]

    def move(self, gamer, i, j):
        self.field[i][j] = gamer + 1

    def cells_legal(self):
        cells_legal_list = []
        for i in range(self.N):
            for j in range(self.N):
                if self.field[i][j] == 0:
                    cells_legal_list.append([i, j])
        print(cells_legal_list)
        return cells_legal_list

    def cells_to_x(self, gamer):
        x = []
        for i in range(self.N):
            for j in range(self.N):
                if self.field[i][j] == 0:
                    x.extend((1, 0, 0))
                elif self.field[i][j] == gamer:
                    x.extend((0, 1, 0))
                else:
                    x.extend((0, 0, 1))
        print(x)
        return x

    def move_legal(self, i, j):
        if self.field[i][j] == 0:
            legal = True
        else:
            legal = False
        return legal

    def round_over_check(self):
        over = True
        gamer = 0
        field_transposed = list(map(list, zip(*self.field)))
        field_diagonals = [[], []]
        for i in range(self.N):
            field_diagonals[0].append(self.field[i][i])
            field_diagonals[1].append(self.field[i][self.N - 1 - i])
        for i in range(1, 3):
            for j in self.field:
                if j.count(i) == self.N:
                    gamer = i
                    break
            for j in field_transposed:
                if j.count(i) == self.N:
                    gamer = i
                    break
            for j in field_diagonals:
                if j.count(i) == self.N:
                    gamer = i
                    break
        if gamer == 0:
            for i in self.field:
                if 0 in i:
                    over = False
                    break
        return over, gamer


class Game:
    def __init__(self, options_ai):
        self.OPTIONS_AI = options_ai
        self.GAMERS = [Gamer('X'), Gamer('O')]
        self.TURN_MOVE_START = int(input('Кто ходит первым? (X - 1 / O - 2) ')) - 1
        self.AI = AI(self.OPTIONS_AI.NEURAL_NETS[self.OPTIONS_AI.neural_nets_type])

        self.field = Field()
        self.score = [0, 0]
        self.turn_move_current = self.TURN_MOVE_START
        self.turn_move_round = self.turn_move_current

    def turn_move_change(self, turn_move):
        if turn_move == 0:
            turn_move = 1
        else:
            turn_move = 0
        return turn_move

    def print_ai_options_w(self):
        for i in range(len(self.ai)):
            for j in range(len(self.ai[i])):
                print('Нейроная сеть: ' + str(i) + '.' + str(j) + '\n' + self.ai[i][j].print_w())

    def __str__(self):
        return '%s %s:%s %s \n %s' % (self.GAMERS[0], self.score[0], self.score[1], self.GAMERS[1], self.field)

    def start(self):
        game_next = True
        while game_next:
            self.round_start()
            game_next = (int(input('Играть еще раз? (1 - Да / 2 - Нет) ')) == 1)
            if game_next == 1:
                self.round_new()
            else:
                self.finish()

    def finish(self):
        pass

    def round_start(self):
        self.field.clear()
        self.turn_move_current = self.turn_move_round
        self.round()

    def round(self):
        round_end = False
        while not round_end:
            print(self)
            self.field.move(self.turn_move_current, *self.GAMERS[self.turn_move_current].move(self.field, self.AI, self.turn_move_current))
            self.turn_move_current = self.turn_move_change(self.turn_move_current)
            round_end, gamer = self.field.round_over_check()
            if round_end:
                self.round_over(gamer)

    def round_over(self, gamer):
        result = ''
        if gamer == 0:
            result = 'Ничья'
        else:
            self.score[gamer - 1] += 1
            result = 'Победил %s %s\n' % (self.GAMERS[gamer - 1], self.GAMERS[gamer - 1].CHAR)
        #         if gamer == 1:
        #             self.GAMERS[0].ii_train(1)
        #             self.GAMERS[1].ii_train(-1)
        #         elif gamer == 2:
        #             self.GAMERS[0].ii_train(-1)
        #             self.GAMERS[1].ii_train(1)
        print(self)
        print(result)

    def round_new(self):
        # self.GAMERS[0].CPU.moves = []
        # self.GAMERS[1].CPU.moves = []
        self.turn_move_round = self.turn_move_change(self.turn_move_round)

    def test(self):
        next = True
        while next:
            self.print_ai_options_w()
            x = list(map(int, input('x = ').split()))
            y = []
            for i in range(len(self.ai)):
                y.append([])
                for j in range(len(self.ai[i])):
                    y[i].append(self.ai[i][j].activate(x))
            print(y)
            y_real = int(input('y = '))
            if y_real != y[0][0]:
                for i in range(len(self.ai)):
                    for j in range(len(self.ai[i])):
                        self.ai[i][j].study(x, y[0][0], y_real)
