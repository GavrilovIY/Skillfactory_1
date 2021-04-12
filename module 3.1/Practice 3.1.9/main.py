from geometry_figure import Rectangle, Square, Circle


if __name__ == '__main__':
    rect_1 = Rectangle(1, 2, 3, 4)
    rect_2 = Rectangle(3, 5, 12, 5)

    print(rect_1.get_area())
    print(rect_2.get_area())

    square_1 = Square(1, 1, 5)
    square_2 = Square(1, 1, 10)

    print(square_1.get_area_square(),
          square_2.get_area_square())

    circle_1 = Circle(1, 1, 5)
    circle_2 = Circle(1, 1, 7)

    figures = [rect_1, rect_2, square_1, square_2, circle_1, circle_2]
    for figure in figures:
        if isinstance(figure, Square):
            print(figure.get_area_square())
        elif isinstance(figure, Rectangle):
            print(figure.get_area())
        else:
            print(figure.get_area_circle())

    rect_3 = Rectangle(5, 10, 50, 100)
    rect_3.print_data_rectangle()