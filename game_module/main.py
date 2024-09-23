from random import randint

from classes import Ship, GamePole, SeaBattle

# def create_ship() -> Ship:
#     length = int(input('Выберите размерность корабля (число от 1 до 4): '))
#     tp = int(input('Выберите ориентацию корабля на игровом поле (1 - горизонтальная, 2 - вертикальная): '))
#     x = int(input('Введите начальную координату расположения корабля по горизонтали: '))
#     y = int(input('Введите начальную координату расположения корабля по вертикали: '))
#     ship = Ship(length, tp, x, y)

#     return ship

def take_action(battle, pole, user=True):
    if user:
        x = int(input(f'Введите координату расположения корабля по горизонтали в диапазоне от 0 до {pole._size - 1}: '))
        y = int(input(f'Введите координату расположения корабля по вертикали в диапазоне от 0 до {pole._size - 1}: '))
        if x not in range(pole._size) or y not in range(pole._size):
            print('Неверные координаты! Попробуйте снова!')
            take_action(battle, pole, user)

    else:
        x = randint(0, pole._size - 1)
        y = randint(0, pole._size - 1)

    is_hit = battle.take_shot(pole, x, y)
    pole.show()
    print()
    if is_hit:
        take_action(battle, pole, user)


def main():
    pole_size = 10

    # Инициализация поля пользователя
    user_game_pole = GamePole(pole_size)
    user_game_pole.init()
    user_game_pole.show()

    print()

    # Инициализация поля компьютера
    environment_game_pole = GamePole(pole_size)    
    environment_game_pole.init()
    environment_game_pole.show()

    current_battle = SeaBattle(user_game_pole._pole, environment_game_pole._pole)

    while environment_game_pole._ships and user_game_pole._ships:
        take_action(current_battle, environment_game_pole)
        # environment_game_pole.show()

        print()

        take_action(current_battle, user_game_pole, user=False)
        # user_game_pole.show()


if __name__ == '__main__':
    main()