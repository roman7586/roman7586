

class UserMail:
    def __init__(self, login, email):
        self.login = login
        self.__email = email

    def get_email(self):
        return self.__email

    def set_email(self, adress):
        if isinstance(adress, str) and adress.count('@') == 1 and "." in adress[adress.find("@"):]:
            self.__email = adress
        else:
            print("Ошибочная почта")

    email = property(fget=get_email, fset=set_email)

from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #Тогда, чтобы проверить, находится ли точка в списке, достаточно просто \
        #       использовать оператор in , как мы делали это с числами .
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

class Ship:
    #    класс Ship - корабль на игровом поле, который описывается параметрами:
    #    1. Длина.
    #    2. Точка, где размещён нос корабля.
    #    3. Направление корабля (вертикальное/горизонтальное)
    #    4. Количеством жизней (сколько точек корабля еще не подбито).
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    #    И имеет методы:
    #    1. Метод dots , который возвращает список всех точек корабля.
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    # 1. Двумерный списк, в котором хранятся состояния каждой из клеток.
    # 2. Список кораблей доски.
    # 3. Параметр hid типа bool - информация о том, нужно ли скрывать корабли на
    # доске (для вывода доски врага), или нет (для своей доски).
    # 4. Количество живых кораблей на доске.
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []
    # И имеет методы:
    # 1. Метод add_ship , который ставит корабль на доску (если ставить не
    #    получается, выбрасываем исключения).
    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)
    # 2. Метод contour , который обводит корабль по контуру. Он будет полезен и в
    # ходе самой игры, и в при расстановке кораблей (помечает соседние точки,
    # где корабля по правилам быть не может).
    def contour(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n                    {i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    # 3. Метод, который выводит доску в консоль в зависимости от параметра hid .
    # 4. Метод out , который для точки (объекта класса Dot ) возвращает True , если
    # точка выходит за пределы поля, и False , если не выходит.
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    # 5. Метод shot , который делает выстрел по доске (если есть попытка
    # выстрелить за пределы и в использованную точку, нужно выбрасывать исключения).
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player:
    # 1. Собственная доска (объект класса Board )
    # 2. Доска врага.
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    # И имеет следующие методы:
    # 1. ask - метод, который "спрашивает" игрока, в какую клетку он делает выстрел.
    # Пока мы делаем общий для AI и пользователя класс, этот метод мы описать
    # не можем. Оставим этот метод пустым. Тем самым обозначим, что потомки
    def ask(self):
        raise NotImplementedError()

    # 2. move - метод, который делает ход в игре. Тут мы вызываем метод ask ,
    # делаем выстрел по вражеской доске (метод Board.shot ), отлавливаем
    # исключения, и если они есть, пытаемся повторить ход. Метод должен
    # возвращать True , если этому игроку нужен повторный ход (например если он
    # выстрелом подбил корабль).
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

# 3. Игрок-компьютер, объект класса Ai .

class AI(Player):
    #Попробовать дописать код, чтобы исключать координаты куда комп уже стрелял. Создать пустой список, /
    #каждый ход сверять со списком и добавлять координаты след.хода. Если координаты есть в ранее /
    # сделанных ходах, сгенерировать новые координаты
    def ask(self):
        d = Dot(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d

# 1. Игрок-пользователь, объект класса User .
class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    # 1. random_board - метод генерирует случайную доску. Для этого мы просто
    # пытаемся в случайные клетки изначально пустой доски расставлять корабли
    # (в бесконечном цикле пытаемся поставить корабль в случайную току, пока
    # наша попытка не окажется успешной). Лучше расставлять сначала длинные
    # корабли, а потом короткие. Если было сделано много (несколько тысяч)
    # попыток установить корабль, но это не получилось, значит доска неудачная и
    # на неё корабль уже не добавить. В таком случае нужно начать генерировать
    # новую доску.
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 5000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    # 2. greet - метод, который в консоли приветствует пользователя и рассказывает
    # о формате ввода.
    def greet(self):
        print("-------------------")
        print("       Игра        ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    # 3. loop - метод с самим игровым циклом. Там мы просто последовательно
    # вызываем метод move для игроков и делаем проверку, сколько живых
    # кораблей осталось на досках, чтобы определить победу.
    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print(f'Доска пользователя: {self.us.board}')
            print("-" * 20)
            print(f'Доска компьютера:   {self.ai.board}')
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    # 4. start - запуск игры. Сначала вызываем greet , а потом loop .
    # И останется просто создать экземпляр класса Game и вызвать метод start .
    # По ходу написания кода полезно проверять свой прогресс, тестируя написанные классы
    # по отдельности. Для этого можно моделировать различные ситуации, например, создать
    # список кораблей, добавить их на доску и попробовать сделать выстрел в разные точки.
    # Для проверки функционала класса не обязательно иметь весь написанный код
    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()