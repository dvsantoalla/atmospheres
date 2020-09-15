import unittest

import studios
import studios.studio01


class TestStudios(unittest.TestCase):

    def test01(self):
        s = studios.studio01.Studio01()
        s.play()
