import unittest
import logging as log
import studios
import studios.studio01

print dir(studios)

class TestStudios(unittest.TestCase):
    def test01(self):
        s = studios.studio01.Studio01()
        s.play()
 	


