from random import choice as AI_choice
import re

from Game_part import Dot, Ship, Board, Out_Of_Boundary, Dot_Is_Busy


class Player:
    def __init__(self, board):
        self.player_board = board
        self.opponent_board = Board(6, hid=False)
        desk_point = []
        for i in range(0, 60, 10):
            for j in range(6):
                desk_point.append(i + j)
        ships = [3, 2, 1, 1, 1, 1]
        orientation = ['V', 'H']
        while True:
            try:
                dot = Board.random_point(desk_point)
                orientation_rand = AI_choice(orientation)
                ship = Ship(size=ships[0], coord=dot, orientation=orientation_rand)
                self.player_board.add_ship(ship)
                self.player_board.ship_contour(ship)
                ships.pop(0)
                # print(ships, i)
                if not desk_point:
                    raise IndexError
                if not ships:
                    break
            except Out_Of_Boundary:
                # print(f'Корабль находится за пределеами доски {dot}, {orientation_rand} ')
                continue
            except Dot_Is_Busy:
                # print(f'Данная точка занята {dot}, {desk_point}')
                continue

    def ask(self):
        pass

    def move(self, opponent_board):
        point = self.ask()
        alive_ship, del_ship = opponent_board.shot(point)
        if alive_ship != -1:
            self.opponent_board.board[point.x][point.y] = 'X'
            if del_ship:
                self.opponent_board.ship_contour(del_ship, 'T')
            return True
        else:
            self.opponent_board.board[point.x][point.y] = 'T'
            return False


class User(Player):
    def ask(self):
        input_data = input("""Введите координаты от 0 до 5 через любой разделитель 
                    (1-ый элемент это строка, 2-ой это столбец). Пример: 0,1 или 0 1 или 0; 1""")
        try:
            shot = tuple(map(int, re.findall(r"[\w']+", input_data)))
            if len(shot) > 2:
                print('Введен лишний элемент')
                raise IndexError
        except ValueError:
            print('Введеное значение не возможно преобраховать в координаты\n')
            raise ValueError
        return Dot(shot[0], shot[1])


class AI(Player):
    def __init__(self, board):
        super().__init__(board)
        self.shot_point = []
        for i in range(0, 60, 10):
            for j in range(6):
                self.shot_point.append(i + j)

    def ask(self):
        return Board.random_point(self.shot_point)


class Game:
    def __init__(self):
        self.user = User(Board(6, hid=False))
        self.ai_bot = AI(Board(6, hid=True))

    @staticmethod
    def greet():
        print('Сейчас будут созданы игровые поля с кораблями, которые расположены на нем случайным образом.')
        print('Первым отрисуется Ваше поле, а по второму мы будем полить из пушек по короблям опонента')
        print("""Для того, что бфы выстрелить необходимо ввести координату на полу от 1 до 6, 
        по столбцам и строкам, через запятую (Пример: 1,4)""")
        print('Давай по играем!!!!!')

    def loop(self):
        print('Доска с вашими кораблями')
        print(self.user.player_board)
        print('А вот доска на которой мы будем искать корабли оппонента')
        print(self.user.opponent_board)
        AI_bot = False
        while True:
            if not AI_bot:
                try:
                    check = self.user.move(self.ai_bot.player_board)
                    if check:
                        if self.ai_bot.player_board.alive_ship != 0:
                            print(f'Количество живых кораблей: {self.ai_bot.player_board.alive_ship}')
                            print(self.user.opponent_board)
                            continue
                        else:
                            print('Враг повержен!!!!')
                            break
                except Dot_Is_Busy:
                    print('Данная ячейка уже занята')
                    continue
                except IndexError:
                    continue
                except ValueError:
                    continue
                except Out_Of_Boundary:
                    print('Попытка выстрелить за пределы поля')
                    continue
                # print(self.ai_bot.player_board)
                print(self.user.opponent_board)
                AI_bot = True
            else:
                try:
                    if self.ai_bot.move(self.user.player_board):
                        AI_bot = True
                        if self.user.player_board.alive_ship != 0:
                            print(f'Количество живых кораблей: {self.user.player_board.alive_ship}')
                            continue
                        else:
                            print('Вы проиграли, рандому:(')
                            break
                except Dot_Is_Busy:
                    print('Данная ячейка уже занята')
                    AI_bot = True
                    continue
                except IndexError:
                    AI_bot = True
                    continue
                except ValueError:
                    AI_bot = True
                    continue
                except Out_Of_Boundary:
                    print('Попытка выстрелить за пределы поля')
                    AI_bot = True
                    continue
                print(self.user.player_board)
                # print(self.ai_bot.opponent_board)
                AI_bot = False

    def start(self):
        self.greet()
        self.loop()









