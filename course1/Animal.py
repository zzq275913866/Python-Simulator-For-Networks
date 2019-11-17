class Animal:
    _sound = ''

    def __init__(self):
        self._sound = '"Animal!"'

    def makesound(self):
        print('%s\n' % self._sound)
