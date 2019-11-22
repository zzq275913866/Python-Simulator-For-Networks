class Animal:
    def __init__(self):
        self._sound = "Animal!"

    def make_sound(self):
        print(self._sound)


class Cat:
    def __init__(self):
        self._sound = "Meow!"

    def make_sound(self):
        print(self._sound)


class Dog:
    def __init__(self):
        self._sound = "Wang!"

    def make_sound(self):
        print(self._sound)


class Woof:
    def __init__(self):
        self._sound = "Woof!"

    def make_sound(self):
        print(self._sound)


# def make_sound(obj):
#     obj.make_sound()


if __name__ == '__main__':
    animal_a = Cat()
    animal_b = Dog()
    animal_c = Woof()
    animals = [animal_a, animal_b, animal_c]
    for an_animal in animals:
        an_animal.make_sound()
