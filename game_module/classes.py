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
        
    def __setitem__(self, indx, value):
        if self.validate_indx(indx):
            self._cells[indx] = value
    
    def validate_indx(self, indx):
        return indx in range(self._length)

    def set_start_coords(self, x, y) -> None:
        """Метод установки начальных координат корабля."""

        if x not in range(10) or y not in range(10):
            raise ValueError('Неверные координаты корабля')
        self._x = x
        self._y = y

    def get_start_coords(self) -> tuple:
        """Метод для получения начальных координат корабля."""

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
        """Метод для проверки корректности расположения кораблей относительно границ игрового поля."""

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
        self._user_pole = list()
        self._opponent_pole = list()

    def init(self):
        """Метод инициализации игрового поля и расстановки кораблей."""

        self._user_pole = [['.' for _ in range(self._size)] for _ in range(self._size)]
        self._opponent_pole = [['.' for _ in range(self._size)] for _ in range(self._size)]

        self._ships = [Ship(5 - i, randint(1, 2)) for i in range(1, 5) for _ in range(i)]

        not_collision_ships = list()

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
            self._user_pole[y][x:x + length] = cells
        else:
            for i in range(y, y + length):
                self._user_pole[i][x] = length

    def get_ships(self):
        return self._ships

    def move_ships(self):
        pass

    def show(self, pole):
        """Метод для отображения игрового поля."""
        [print(*[cell for cell in row]) for row in pole]

    # def get_pole(self):
    #     return tuple(tuple(cell for cell in row) for row in self._pole)


class SeaBattle:
    """Класс управления игровым процессом."""

    # def __init__(self, user_pole: GamePole, opponent_pole: GamePole):
    #     self.user_pole = user_pole
    #     self.opponent_pole = opponent_pole

    @staticmethod
    def mark_target(target_pole: GamePole, current_pole: GamePole, ship: Ship, x: int, y: int, tp: int):
        """Статический метод для отметки изменения состояния корабля."""

        target_pole._pole[y][x] = 'X'
        current_pole._opponent_pole[y][x] = 'X'

        if tp == 1:
            ship[x - ship._x] = 'X'
        else:
            ship[y - ship._y] = 'X'

        if set(ship._cells) == {'X'}:
            target_pole._ships.remove(ship)

            if tp == 1:
            #     if ship._x == 0:
            #         if ship._y == 0:
            #             current_pole._opponent_pole[ship._y + 1][ship._x:ship._x + ship._length + 1] = '*'
            #             for i in range(ship._y, ship._y + 2):
            #                 current_pole._opponent_pole[i][ship._x + ship._length] = '*'
            #         elif ship._y == current_pole._size - 1:
            #             current_pole._opponent_pole[ship._y - 1][ship._x:ship._x + ship._length + 1] = '*'
            #             for i in range(ship._y - 1, ship._y + 1):
            #                 current_pole._opponent_pole[i][ship._x + ship._length] = '*'
            #     elif ship._y == 0:
            #         if ship._x == current_pole._size - 1:

                
                
                current_pole._opponent_pole[ship._y][ship._x - int(ship._x != 0)] = '*'
                current_pole._opponent_pole[ship._y][ship._x + ship._length - (int(ship._x + ship._length) == current_pole._size)] = '*'
                for i in range(ship._x - int(ship._x != 0), ship._x + ship._length + int(ship._x != current_pole._size - 1)):
                    current_pole._opponent_pole[y - int(ship._y != 0)][i] = '*'
                    current_pole._opponent_pole[y + int(ship._y != current_pole._size - 1)][i] = '*'

                # current_pole._opponent_pole[ship._y - int(ship._y != 0)][ship._x - int(ship._x != 0): ship._x + ship._length + int(ship._x != current_pole._size - 1)] = ['E'] * (ship._length + int(ship._x != 0) + int(ship._x != current_pole._size - 1))
                # current_pole._opponent_pole[ship._y][ship._x - int(ship._x != 0)] = 'E'
                # current_pole._opponent_pole[ship._y][ship._x + ship._length] = 'E'
                # current_pole._opponent_pole[ship._y + int(ship._y != current_pole._size - 1)][ship._x - int(ship._x != 0): ship._x + ship._length + int(ship._x != current_pole._size - 1)] = ['E'] * (ship._length + int(ship._x != 0) + int(ship._x != current_pole._size - 1))
            else:
                current_pole._opponent_pole[ship._y - int(ship._y != 0)][ship._x] = '*'
                current_pole._opponent_pole[ship._y + ship._length - (int(ship._y + ship._length) == current_pole._size)][ship._x] = '*'
                for i in range(ship._y - 1, ship._y + ship._length + int(ship._y != current_pole._size - 1)):
                    current_pole._opponent_pole[i][x - int(ship._x != 0)] = '*'
                    current_pole._opponent_pole[i][x + int(ship._x != current_pole._size - 1)] = '*'

    def take_shot(self, target_pole: GamePole, current_pole: GamePole, x: int, y: int):
        """Метод для совершения атаки."""

        flag = False
        for ship in target_pole._ships:
            if ship._tp == 1 and x in range(ship._x, ship._x + ship._length) and y == ship._y:
                self.mark_target(target_pole, current_pole, ship, x, y, tp=1)
                flag = True
                break

            elif ship._tp == 2 and y in range(ship._y, ship._y + ship._length) and x == ship._x:
                self.mark_target(target_pole, current_pole, ship, x, y, tp=2)
                flag = True
                break
        else:
            target_pole._pole[y][x] = '*'
            current_pole._opponent_pole[y][x] = '*'

        return flag
