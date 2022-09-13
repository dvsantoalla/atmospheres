import unittest

import studios
import studios.studio01
import studios.studio02


class TestStudios(unittest.TestCase):

    def test01(self):
        s = studios.studio01.Studio01()
        s.play()

    def no_test02(self):
        s = studios.studio02.Studio02()
        s.play()
