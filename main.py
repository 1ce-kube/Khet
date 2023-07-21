
# = Imports
from prettytable import PrettyTable # Надо установить библиотеку | pip install prettytable
from colorama import Fore, Back

# = Variables

figures = {
    "U1" : [
        {"type": "laser", "direction": "N", "location": (7, 7)},
        {"type": "king", "direction": "N", "location": (6, 6)},
        {"type": "key", "direction": "S", "location": (7, 4)}, # \
    ],
    "U2" : [
        {"type": "laser", "direction": "S", "location": (0, 0)},
        {"type": "king", "direction": "S", "location": (1, 4)},
        {"type": "key", "direction": "N", "location": (0, 1)},
    ]
}
"""
Фигуры пользователей

Имеет 3 параметра:
- Тип - один из типов фигуры
- Размещение (set из 2х значений - координат на доске (col, row))
- Направление - одно из 4х направлений:

```
        N
      W   E
        S
```
"""

field = {}
""" 
Поле, размером 8×8. Сначала указывается значение X (столбец), далее Y (строка) с помощью типа set
- Переменные X и Y могут принизмать значение от 0 до 7

Сделано не массивом для оптимизации
"""

# = Functions

def set_field():
    """раставляет фигуры в положении, указанном в данных в переменной figures"""

    field.clear()
    
    color = Fore.BLUE
    for user in figures.keys():
        for figure in figures[user]:
            symb = "•"
            if figure["type"] == "laser":
                symb = {"N": "↑", "E": "→", "S": "↓", "W": "←"}[figure["direction"]]
            elif figure["type"] == "king":
                symb = "⁕"
            elif figure["type"] == "key":
                symb = {"N": "\\", "E": "/", "S": "\\", "W": "/"}[figure["direction"]]
            field[figure["location"]] = color + symb + Fore.RESET
        color = Fore.RED

def laser(U:int = 1):
    """Просчитывает  лазер
    
    :param U: Номер игрока (1 or 2)"""
    obj = list(filter(lambda _: _["type"] == "laser", figures[f"U{U}"]))[0]

    # Первая версия просчитки лазера
    # if obj["direction"] == "N" or obj["direction"] == "S":
    #     for row in range(obj["location"][1], -1 if obj["direction"] == "N" else 8, -1 if obj["direction"] == "N" else 1):
    #         loc = ((obj["location"][1]), row)
    #         if loc in field:
    #             field[loc] = Back.CYAN + field[loc] + Back.RESET
    #         else:
    #             field[loc] = Fore.BLUE + Back.CYAN + "|" + Fore.RESET + Back.RESET
    # def fill_matrix(matrix, start_row, start_col, direction):

    start_row, start_col = obj["location"][1], obj["location"][0]
    rows = 8
    cols = 8
    direction = obj["direction"]
    vectors = {
        'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1),
        'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1),
        '↑': (-1, 0), '↓': (1, 0), '←': (0, -1), '→': (0, 1) # Для удобства в прототипе использовал стрелочки
    }
    
    # Вычисление вектора для движения
    vector = vectors[direction]
    row, col = start_row, start_col
    
    while True:
        row += vector[0]
        col += vector[1]
        # Установка символа заполнения в зависимости от горизонтального или вертикального направления
        # fill_symbol = Fore.BLUE + Back.CYAN + "-" + Fore.RESET + Back.RESET if direction in ['left', 'right', '→', '←', "E", "W"] else Fore.BLUE + Back.CYAN + "|" + Fore.RESET + Back.RESET
        colour = Back.CYAN  if U == 1 else Back.MAGENTA 
        fill_symbol = colour + " " + Back.RESET if U == 1 else colour + " " + Back.RESET
        
        # Проверка, что новые координаты находятся в пределах матрицы
        if row < 0 or row >= rows or col < 0 or col >= cols:
            break
        
        # Проверка, что ячейка матрицы пустая
        if (col, row) in list(field.keys()):
            
            if field[(col, row)].replace(Fore.RED, "").replace(Fore.RESET, "").replace(Fore.BLUE, "") == '⁕':
                # Проверка, что ячейка матрицы содержит символ "*", остановка движения
                field[(col, row)] =   Back.YELLOW + field[(col, row)] + Back.RESET
                break

            elif field[(col, row)].replace(Fore.RED, "").replace(Fore.RESET, "").replace(Fore.BLUE, "") == chr(92):
                # Проверка, что ячейка матрицы содержит символ  изменения направления \
                if direction == "S":
                    direction = "E"
                elif direction == "W":
                    direction = "N"
                elif direction == "N":
                    direction = "W"
                else:
                    direction = "S"
                vector = vectors[direction]

                field[(col, row)] =   colour + field[(col, row)] + Back.RESET
            elif field[(col, row)].replace(Fore.RED, "").replace(Fore.RESET, "").replace(Fore.BLUE, "") == "/":
                #  Проверка, что ячейка матрицы содержит символ  изменения направления /
                if direction == "S":
                    direction = "W"
                elif direction == "W":
                    direction = "S"
                elif direction == "N":
                    direction = "E"
                else:
                    direction = "N"
                vector = vectors[direction]

                field[(col, row)] =   colour + field[(col, row)] + Back.RESET
            else:

                # print(field[(col, row)], field[(col, row)] == chr(92))
                pass
        else:
            field[(col, row)] = fill_symbol


def view():
    """выводит таблицу в консоль"""
    field_protorype = []
    for row in range(8):
        for col in range(8):
            if (col, row) in field:
                field_protorype.append(field[(col, row)])
            else:
                field_protorype.append(" ")
    th = [str(i) for i in range(8)]

    table = PrettyTable(th)
    td_data = field_protorype[:]
    while td_data:
        table.add_row(td_data[:len(th)])
        td_data = td_data[len(th):]

    print(table)  # Печатаем таблицу

# = Run

if __name__ == '__main__':
    set_field() # начальная постановка
    laser(1) # просчитка лазера игрока 1
    laser(2) # Просчитка лазера игрока 2
    view() # вывод поля, фигур, лазеров
