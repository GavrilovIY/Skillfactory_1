import re


def create_desk(size=3):
    return [['-'] * size for i in range(size)]


def check_win(func):
    def wrapper(*arg):
        if arg[1] == '-':
            func(*arg)
        else:
            for i in range(len(arg[0][0][:])):
                if arg[0][i][0] == arg[1] and arg[0][i][1] == arg[1] and arg[0][i][2] == arg[1]:
                    func(*arg)
                    print(f"{arg[1]} is winner!!!\n")
                    return 0
                elif arg[0][0][i] == arg[1] and arg[0][1][i] == arg[1] and arg[0][2][i] == arg[1]:
                    func(*arg)
                    print(f"{arg[1]} is winner!!!\n")
                    return 0
                elif arg[0][0][0] == arg[1] and arg[0][1][1] == arg[1] and arg[0][2][2] == arg[1]:
                    func(*arg)
                    print(f"{arg[1]} is winner!!!\n")
                    return 0
                elif arg[0][2][0] == arg[1] and arg[0][1][1] == arg[1] and arg[0][0][2] == arg[1]:
                    func(*arg)
                    print(f"{arg[1]} is winner!!!\n")
                    return 0
                elif '-' not in arg[0][:][0] and '-' not in arg[0][:][1] and '-' not in arg[0][:][2]:
                    func(*arg)
                    print('Ничья!!!!')
                    return 0
                else:
                    func(*arg)
                    return 1
    return wrapper


@check_win
def print_desk(desk, element):
    string = ' 0 1 2\n'
    num = 0
    for i in desk[:]:
        string = string + str(num) + ' '.join(i) + '\n'
        num += 1
    print(string)


def change_element(desk, point, element):
    desk[point[0]][point[1]] = element
    return desk


if __name__ == '__main__':
    play_desk = create_desk()
    print_desk(play_desk, '-')
    cont = 1
    start_name = input('Выберите, кто начинает [X/O]')
    if start_name.lower() == 'x':
        count = 1
    else:
        count = 2
    while cont:
        if count % 2:
            Type = 'X'
        else:
            Type = '0'
        print(f'Ходят {Type}')
        input_data = input("""Введите координаты от 0 до 2 через любой разделитель 
        (1-ый элемент это строка, 2-ой это столбец). Пример: 0,1 или 0 1 или 0; 1""")
        pos = re.findall(r"[\w']+", input_data)
        if len(pos) == 2:
            if pos[0].isdigit() and pos[1].isdigit():
                pos = tuple(map(int, pos))
                if pos[0] == 9:
                    break
                elif pos[0] <= 2 and pos[1] <= 2:
                    if play_desk[pos[0]][pos[1]] == '-':
                        change_element(play_desk, pos, Type)
                        cont = print_desk(play_desk, Type)
                        count += 1
                    else:
                        print(f'В данном месте уже стоит {play_desk[pos[0]][pos[1]]} \n')
                        print('Введите по новой\n')
                        continue
                else:
                    print('Значения за пределами допустимого!!!!!')
                    continue
            else:
                print('Проверьте корректность ввода')
                continue
        else:
            print('Количество элементов должно быть равно 2')
            continue



