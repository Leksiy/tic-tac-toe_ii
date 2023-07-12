import random
import math


class Perceptron:
    def __init__(self, train_speed, function, x_count):
        self.TRAIN_SPEED = train_speed
        self.FUNCTION = function

        self.w = [1] * (x_count + 1)

    def __str__(self):
        return 'w=' + str(self.w)

    @staticmethod
    def sign(x):
        if x > 0:
            y = 1
        else:
            y = -1
        return y

    @staticmethod
    def sigmoid(x):
        y = round((1 / (1 + math.exp(-x))), 2)
        return y

    def activate(self, x):
        x_all = x.copy()
        x_all.append(1)
        y = 0
        for i, j in zip(x, self.w):
            y += i * j
        match self.FUNCTION:
            case 'sign':
                y = self.sign(y)
            case 'sigmoid':
                y = self.sigmoid(y)
        print('per. activate: x=', x_all, 'w=', self.w, 'y=', y, sep='')
        return y

    def study(self, x, y, y_real):
        x_all = x.copy()
        x_all.append(1)
        print('per. study: x=', x_all, 'w=', self.w, 'y=', y, sep='')
        for i in range(len(self.w)):
            self.w[i] = self.w[i] + self.TRAIN_SPEED * (y_real - y) * x_all[i]
        print('per. study: x=', x_all, 'w=', self.w, 'y=', y, sep='')


class NeuralNet:
    def __init__(self, name, level, perceptrons):
        self.NAME = name
        self.LEVEL = level

        self.perceptrons = []
        for i in range(self.LEVEL):
            self.perceptrons.append([])
            for j in range(perceptrons[i][0]):
                self.perceptrons[i].append(Perceptron(perceptrons[i][1], perceptrons[i][2], perceptrons[i][3]))

    def __str__(self):
        about = 'Тип нейросети: ' + self.NAME + '\n'
        about += 'Количество уровней: ' + str(self.LEVEL) + '\n'
        for i in range(self.LEVEL):
            about += 'Уровень ' + str(i + 1) + '\n'
            about += ' ' + 'Количество нейронов  - ' + str(len(self.perceptrons[i])) + '\n'
            about += ' ' + 'Количество дендритов - ' + str(len(self.perceptrons[i][0].w)) + '\n'
            about += ' ' + 'Скорость обучения    - ' + str(self.perceptrons[i][0].TRAIN_SPEED) + '\n'
            about += ' ' + 'Функция активации    - ' + str(self.perceptrons[i][0].FUNCTION) + '\n'
        return about

    def print_w(self):
        w = ''
        for i in range(self.LEVEL):
            for j in range(len(self.perceptrons[i])):
                w += 'Нейрон: ' + str(i) + '.' + str(j) + '\n'
                w += self.perceptrons[i][j].__str__() + '\n'
        return w

    def activate(self, x_real):
        x_next_level = x_real.copy()
        for i in range(self.LEVEL):
            y = []
            for j in range(len(self.perceptrons[i])):
                if j == 0:
                    x_perceptron = x_next_level[:len(self.perceptrons[i][j].w) - 1]
                    x_next_level = x_next_level[len(self.perceptrons[i][j].w) - 1:]
                    y.append(self.perceptrons[i][j].activate(x_perceptron))
                else:
                    y.append(self.perceptrons[i][j].activate(x_next_level))
            x_next_level = y.copy()
        return x_next_level[0]

    def study(self, x, y, y_real):
        self.perceptrons[0][0].study(x, y, y_real)


class AI:
    def __init__(self, neural_net):
        self.neural_net = neural_net
        self.cells_legal_list = []
        self.x = []
        self.y = []

    def __str__(self):
        return 'ИИ:\n' + str(self.neural_net)

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
        return cell

    def study(self, y_real):
        for i in self.moves:
            if i.y != y_real:
                self.neural_net.study(i.x, i.y, y_real)
                print(self.neural_net.print_w())
