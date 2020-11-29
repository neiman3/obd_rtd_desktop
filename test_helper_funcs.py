from unittest import TestCase
from helper_funcs import *

x = 0

class Test(TestCase):

    def test_globals(self):
        global x
        x += 1
    def test_shorten_file_name(self):
        print(x)
        s = shortenStringToFit("Alex neimdnan is the cooelst fuye ever. His coeding skills are immaculate")
        self.fail()

def test():
    Test.test_globals()
    print(x)
