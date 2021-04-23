# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class Square:
    def __init__(self, side):
        self.side = side

    @property
    def square(self):
        return self._side**2

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        if value > 0:
            self._side = value
        else:
            raise ValueError("Side must be more then 0")



class SquareFactory:
    @staticmethod
    def create_square(value):
        return Square(side=value)


# создадим класс собаки
class Dog:
    _happiness = 10

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def human_age(self):
        return self.age * 7.3

    # добавим новое поле - шкала счастья
    @property
    def happiness(self):
        return self._happiness

    # с помощью декоратора setter мы можем неявно передать во второй
    # аргумент значение, находящееся справа от равно, а не закидывать это
    # значение в скобки, как мы это делали в модуле C1, когда не знали о
    # декораторах класса
    @happiness.setter
    # допустим, мы хотим, чтобы счастье питомца измерялось шкалой от 0 до 100
    def happiness(self, value):
        if value <= 100 and value >= 0:
            self._happiness = value
        else:
            raise ValueError("Happiness must be between 0 ... 100")


class ParentClass:

    @classmethod
    def method(cls, arg):
        print("%s classmethod. %d" % (cls.__name__, arg))

    @classmethod
    def call_original_method(cls):
        cls.method(5)

    def call_class_method(self):
        self.method(10)


class ChildClass(ParentClass):

    @classmethod
    def call_original_method(cls):
        cls.method(6)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sq1 = SquareFactory.create_square(10)

    print(sq1.square, sq1.side)
    sq2 = SquareFactory.create_square(2)
    jane = Dog("jane", 4)
    jane.happiness = 90  # осчастливим нашу собаку < :
    print(jane.happiness)

    ParentClass.method(0)  # ParentClassclassmethod. 0
    ParentClass.call_original_method()  # ParentClassclassmethod. 5

    ChildClass.method(0)  # ChildClassclassmethod. 0
    ChildClass.call_original_method()  # ChildClassclassmethod. 6

    # Вызываем методы класса через объект.
    my_obj = ParentClass()
    my_obj.method(1)  # ParentClassclassmethod. 1
    my_obj.call_class_method()  # ParentClassclassmethod. 10


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
