from random import choice as AI_choice


class Out_Of_Boundary(Exception):
    pass


class Dot_Is_Busy(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'<{self.x},{self.y}>'

    def __eq__(self, other):
        if not isinstance(other, Dot):
            raise TypeError('An instance of class Dot is expected')
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if not isinstance(other, Dot):
            raise TypeError('An instance of class Dot is expected')
        return self.x < other.x or self.y < other.y

    def __gt__(self, other):
        if not isinstance(other, Dot):
            raise TypeError('An instance of class Dot is expected')
        return self.x > other.x or self.y > other.y


class Ship:
    def __init__(self, size, coord, orientation):
        self.size = size
        if not isinstance(coord, Dot):
            raise TypeError('An instance of class Dot is expected')
        self.coord = coord
        self.orientation = orientation
        self.dead_elements = []

    @property
    def ship_orientation(self):
        return self.orientation

    @property
    def len_ship(self):
        return self.size

    def get_dots(self):
        if self.orientation == 'V':
            return [Dot(self.coord.x + i, self.coord.y) for i in range(self.size)]
        else:
            return [Dot(self.coord.x, self.coord.y + i) for i in range(self.size)]

    def add_dead_element(self, dot):
        if not isinstance(dot, Dot):
            raise TypeError('An instance of class Dot is expected')
        self.dead_elements.append(dot)

    def get_dead_element(self):
        return self.dead_elements


class Board:
    def __init__(self, board_size, hid):
        self.board = [['\u25CC'] * board_size for i in range(board_size)]
        self.ships = []
        self.hid = hid
        self.number_of_living_ships = 6

    def __str__(self):
        str1 = '  | ' + ' | '.join(map(str, range(0, 6))) + ' |' + '\n'
        count = 0
        for b in self.board[:]:
            str1 = str1 + str(count) + ' | ' + ' | '.join(b) + ' |' + '\n'
            count += 1
        return str1

    @staticmethod
    def out(x, y):
        if Dot(x, y) < Dot(0, 0) or Dot(x, y) > Dot(5, 5):
            return True

    @staticmethod
    def random_point(array_points):
        point = AI_choice(array_points)
        array_points.pop(array_points.index(point))
        dot = Dot(point // 10, point % 10)
        return dot

    @property
    def alive_ship(self):
        return self.number_of_living_ships

    def add_ship(self, ship):
        iterate = 0
        for i in ship.get_dots():
            if self.out(i.x, i.y):
                raise Out_Of_Boundary
            if self.ships:
                for old_ship in self.ships[:-1]:
                    if i in old_ship.get_dots():
                        raise Dot_Is_Busy
            if self.board[i.x][i.y] != '\u25CC':
                raise Dot_Is_Busy
            iterate += 1
        if iterate == len(ship.get_dots()):
            for i in ship.get_dots():
                self.board[i.x][i.y] = '\u2589'
            self.ships.append(ship)

    def ship_contour(self, ship, literal='\u23FA'):
        ship_dots = ship.get_dots()
        if ship.ship_orientation == 'H':
            for j in range(3):
                if not self.out(ship_dots[0].x + j - 1, ship_dots[0].y - 1):
                    self.board[ship_dots[0].x + j - 1][ship_dots[0].y - 1] = literal
                if not self.out(ship_dots[len(ship_dots) - 1].x + j - 1, ship_dots[len(ship_dots) - 1].y + 1):
                    self.board[ship_dots[len(ship_dots) - 1].x + j - 1][ship_dots[len(ship_dots) - 1].y + 1] = literal
            for dot in ship_dots:
                if dot.x == 0:
                    self.board[dot.x + 1][dot.y] = literal
                elif dot.x == 5:
                    self.board[dot.x - 1][dot.y] = literal
                else:
                    self.board[dot.x + 1][dot.y] = literal
                    self.board[dot.x - 1][dot.y] = literal
        else:
            for j in range(3):
                if not self.out(ship_dots[0].x - 1, ship_dots[0].y + j - 1):
                    self.board[ship_dots[0].x - 1][ship_dots[0].y + j - 1] = literal
                if not self.out(ship_dots[len(ship_dots) - 1].x + 1, ship_dots[len(ship_dots) - 1].y + j - 1):
                    self.board[ship_dots[len(ship_dots) - 1].x + 1][ship_dots[len(ship_dots) - 1].y + j - 1] = literal
            for dot in ship_dots:
                if dot.y == 0:
                    self.board[dot.x][dot.y + 1] = literal
                elif dot.y == 5:
                    self.board[dot.x][dot.y - 1] = literal
                else:
                    self.board[dot.x][dot.y + 1] = literal
                    self.board[dot.x][dot.y - 1] = literal

    def shot(self, point):
        # try:
        if self.out(point.x, point.y):
            raise Out_Of_Boundary
        if self.ships:
            for ship in self.ships:
                if point in ship.get_dots():
                    if point in ship.get_dead_element():
                        raise Dot_Is_Busy
                    self.board[point.x][point.y] = 'X'
                    ship.add_dead_element(point)
                    del_ship = self.del_ship(ship)
                    if del_ship:
                        self.ship_contour(del_ship, 'T')
                    return self.alive_ship, del_ship
            if self.board[point.x][point.y] == 'T':
                raise Dot_Is_Busy
            self.board[point.x][point.y] = 'T'
            return -1, None

    def del_ship(self, ship):
        if len(ship.get_dead_element()) == ship.len_ship:
            self.number_of_living_ships -= 1
            return ship
