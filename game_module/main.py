from random import randint

from classes import Ship, GamePole, SeaBattle

# def create_ship() -> Ship:
#     length = int(input('Выберите размерность корабля (число от 1 до 4): '))
#     tp = int(input('Выберите ориентацию корабля на игровом поле (1 - горизонтальная, 2 - вертикальная): '))
#     x = int(input('Введите начальную координату расположения корабля по горизонтали: '))
#     y = int(input('Введите начальную координату расположения корабля по вертикали: '))
#     ship = Ship(length, tp, x, y)

#     return ship


def take_action(battle: SeaBattle, target_pole: GamePole, current_pole: GamePole, user=True):
    if user:
        x = int(input(f'Введите координату расположения корабля по горизонтали в диапазоне от 0 до {target_pole._size - 1}: '))
        y = int(input(f'Введите координату расположения корабля по вертикали в диапазоне от 0 до {target_pole._size - 1}: '))
        if x not in range(target_pole._size) or y not in range(target_pole._size):
            print('Неверные координаты! Попробуйте снова!')
            take_action(battle, target_pole, current_pole, user)

    else:
        x = randint(0, target_pole._size - 1)
        y = randint(0, target_pole._size - 1)

    is_hit = battle.take_shot(target_pole, current_pole, x, y)
    if user:
        print('User Pole')
        current_pole.show(current_pole._pole)
        print()
        print('Opponent Pole for User')
        current_pole.show(current_pole._opponent_pole)

    # print()
    if is_hit:
        take_action(battle, target_pole, current_pole, user)


def main():
    pole_size = 10

    # Инициализация поля пользователя
    user_pole = GamePole(pole_size)
    user_pole.init()

    # Инициализация поля компьютера
    opponent_pole = GamePole(pole_size)    
    opponent_pole.init()
    # environment_game_pole.show()

    current_battle = SeaBattle()

    while user_pole._ships and opponent_pole._ships:
        print('User Pole')
        user_pole.show(user_pole._pole)
        print()
        print('Opponent Pole for User')
        user_pole.show(user_pole._opponent_pole)

        take_action(current_battle, opponent_pole, user_pole)

        take_action(current_battle, user_pole, opponent_pole, user=False)


if __name__ == '__main__':
    main()