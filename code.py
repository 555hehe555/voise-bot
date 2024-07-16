
import numpy as np

# Матрица игрового поля
field = np.zeros((3, 3), dtype=int)

# Функция проверки победы
def check_win (player):
    for i in range(3):
        if field[i, 0] == player and field[i, 1] == player and field[i, 2] == player:
            return True
        if field[0, i] == player and field[1, i] == player and field[2, i] == player:
            return True
    if field[0, 0] == player and field[1, 1] == player and field[2, 2] == player:
        return True
    if field[0, 2] == player and field[1, 1] == player and field[2, 0] == player:
        return True
    return False

# Функция искусственного интеллекта
def ai_move():
    for i in range(3):
        for j in range(3):
            if field[i, j] == 0:
                field[i, j] = 1
                if check_win(1):
                    return
                field[i, j] = 0
    for i in range(3):
        for j in range(3):
            if field[i, j] == 0:
                field[i, j] = 2
                if check_win(2):
                    return
                field[i, j] = 0
    # Если блокируются победы, выбираем центр поля
    for i in range(3):
        for j in range(3):
            if field[i, j] == 0:
                field[i, j] = 1
                return
    # Если центр поля не доступен, выбираем случайный ход
    while True:
        i = np.random.randint(0, 3)
        j = np.random.randint(0, 3)
        if field[i, j] == 0:
            field[i, j] = 1
            return

# Функция игрокового хода
def player_move(i, j):
    if field[i, j] == 0:
        field[i, j] = 2
    else:
        print("Данный ход уже был сделан. Пожалуйста, выборите другой ход.")

# Главная функция игры
def main():
    while True:
        print(np.array(field, dtype=object))
        i = int(input("Введите номер строки для игрока: "))
        j = int(input("Введите номер столбца для игрока: "))
        player_move(i, j)
        if check_win(2):
            print("Игрок выиграл!")
            break
        ai_move()
        if check_win(1):
            print("Искусственный интеллект выиграл!")
            break

main()
