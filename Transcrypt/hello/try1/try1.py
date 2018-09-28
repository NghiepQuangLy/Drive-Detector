from itertools import chain


def setting1():
    constants = 20


def setting2():
    constants = 30
    return constants


class PrintIt:
    def __init__(self):
        self.output = 0

    def get_output(self):
        self.output = setting2()
        document.getElementById('printing_area').innerHTML = self.output


instance_of_class = PrintIt()


