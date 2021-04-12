import math as M


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height

    def print_data_rectangle(self):
        print(f'Rectangle({self.x}, {self.y}, {self.width}, {self.height})')


class Square:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

    def get_area_square(self):
        return self.width**2

    def print_data_square(self):
        print(f'Square({self.x}, {self.y}, {self.width})')


class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def get_area_circle(self):
        return M.pi*self.r**2

    def print_data_circle(self):
        print(f'Circle({self.x}, {self.y}, {self.r})')
