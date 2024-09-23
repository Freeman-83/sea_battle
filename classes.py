from random import randint


class Ship:
    """Класс корабля."""

    def __init__(self, length: int, tp=1, x=None, y=None) -> None:
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [self._length] * self._length

    def __getitem__(self, indx):
        if self.validate_indx(indx):
            return self._cells[indx]
        
    def __setitem__(self, indx, value='*'):
        if self.validate_indx(indx):
            self._cells[indx] = value
    
    def validate_indx(self, indx):
        return indx in range(self._length)

    def set_start_coords(self, x, y) -> None:
        if x not in range(10) or y not in range(10):
            raise ValueError('Неверные координаты корабля')
        self._x = x
        self._y = y

    def get_start_coords(self) -> tuple:
        """Метод для получения стартовых координат корабля."""
        return self._x, self._y
    
    def move(self, go: int) -> None:
        if self._is_move:
            if self._tp == 1:
                self._x += go
            else:
                self._y += go

    def is_collide(self, ship) -> bool:
        """Метод для проверки корректности расположения кораблей относительно друг друга."""

        if self._tp == 1:
            if ship._tp == 1:
                return all(
                    [set(range(self._x, self._x + self._length)) & set(range(ship._x - 1, ship._x + ship._length + 1)),
                     self._y in range(ship._y - 1, ship._y + 2)]
                )
            return all(
                [set(range(self._x, self._x + self._length)) & set(range(ship._x - 1, ship._x + 2)),
                 self._y in range(ship._y - 1, ship._y + ship._length + 1)]
            )

        elif ship._tp == 1:
            return all(
                [self._x in range(ship._x - 1, ship._x + ship._length + 1),
                 set(range(self._y, self._y + self._length)) & set(range(ship._y - 1, ship._y + 2))]
            )
        return all(
            [set(range(self._y, self._y + self._length)) & set(range(ship._y - 1, ship._y + ship._length + 1)),
             self._x in range(ship._x - 1, ship._x + 2)]
        )
        
    def is_out_pole(self, size):
        """Метод для проверки корректности расположения кораблей границ игрового поля."""
        if self._tp == 1:
            return self._x + self._length > size
        return self._y + self._length > size
        
    def __str__(self) -> str:
        return f'{self._length}, {self._x}, {self._y}, {self._cells}'
        

class GamePole:
    """Класс игрового поля."""

    def __init__(self, size: int):
        self._size = size
        self._ships: list[Ship] = list()
        self._pole = list()

    def init(self):
        """Метод инициализации игрового поля и расстановки кораблей."""

        self._pole = [[0 for _ in range(self._size)] for _ in range(self._size)]
        self._ships = [Ship(5 - i, randint(1, 2)) for i in range(1, 5) for _ in range(i)]

        not_collision_ships = []

        i = 0
        while i < self._size:

            if not not_collision_ships:
                self._ships[i]._x, self._ships[i]._y = randint(0, self._size - 1), randint(0, self._size - 1)
                while self._ships[i].is_out_pole(self._size):
                    self._ships[i]._x, self._ships[i]._y = randint(0, self._size - 1), randint(0, self._size - 1)

            else:
                flag = True
                while flag:
                    for checked_ship in not_collision_ships:
                        if self._ships[i] != checked_ship:
                            if not self._ships[i]._x and not self._ships[i]._y:
                                self._ships[i]._x, self._ships[i]._y = randint(0, self._size - 1), randint(0, self._size - 1)
                            if self._ships[i].is_collide(checked_ship) or self._ships[i].is_out_pole(self._size):
                                self._ships[i]._x, self._ships[i]._y = None, None
                                break
                    else:
                        flag = False

            not_collision_ships.append(self._ships[i])

            i += 1

        self._ships = not_collision_ships[:]

        for ship in not_collision_ships:
            self.set_ship(ship._x,
                          ship._y,
                          ship._length,
                          ship._tp,
                          ship._cells)

    def set_ship(self, x, y, length, tp, cells):
        """Метод для установки корабля на выбранную позицию."""
        if tp == 1:
            self._pole[y][x:x + length] = cells
        else:
            for i in range(y, y + length):
                self._pole[i][x] = length

    def get_ships(self):
        return self._ships

    def move_ships(self):
        pass

    def show(self):
        """Метод для отображения игрового поля."""
        [print(*[cell for cell in row]) for row in self._pole]

    # def get_pole(self):
    #     return tuple(tuple(cell for cell in row) for row in self._pole)


class SeaBattle:
    """Класс управления игровым процессом."""

    def __init__(self, user_game_pole: GamePole, environment_game_pole: GamePole):
        self.user_game_pole = user_game_pole
        self.environment_game_pole = environment_game_pole

    @staticmethod
    def mark_target(pole, ship, x, y):
        pole._pole[y][x] = 'X'
        ship._cells[x - ship._x] = 'X'
        if set(ship._cells) == {'X'}:
            pole._ships.remove(ship)

    def take_shot(self, pole: GamePole, x: int, y: int):
        flag = False
        for ship in pole._ships:
            if ship._tp == 1 and x in range(ship._x, ship._x + ship._length) and y == ship._y:
                self.mark_target(pole, ship, x, y)
                flag = True
                break

            elif ship._tp == 2 and y in range(ship._y, ship._y + ship._length) and x == ship._x:
                self.mark_target(pole, ship, x, y)
                flag = True
                break

        else:
            pole._pole[y][x] = '*'

        return flag


        
