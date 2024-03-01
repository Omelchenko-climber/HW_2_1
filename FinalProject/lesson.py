from abc import abstractmethod, ABC


class Shape(ABC):
    @abstractmethod
    def square_of(self):
        pass

    @abstractmethod
    def perimetr(self):
        pass


class Rect(Shape):
    def __init__(self, side_a, side_b):
        self.side_a = side_a
        self.side_b = side_b

    def square_of(self):
        square = self.side_a * self.side_b
        return square

    def perimetr(self):
        perimetr = self.side_a + self.side_b
        return perimetr


rect = Rect(2, 3)
print(rect.square_of())
print(rect.perimetr())
print(type(int))

from random import randint


class Common:
    def __init__(self):
        self.param = randint(1, 10)


class SingleMeta():
    is_instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.is_instance:
            cls.is_instance = super().__class__(cls, *args, **kwargs)
            return cls.is_instance
        else:
            return cls.is_instance


class SingleClass(SingleMeta):
    def __init__(self):
        self.param = randint(1, 10)


for i in range(10):
    cm = Common()
    print(f'{cm.param = }')

    sc = SingleClass()
    print(f'{sc.param = }')