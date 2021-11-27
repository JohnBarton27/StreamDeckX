import unittest
from unittest.mock import patch


class BaseStreamdeckXTest(unittest.TestCase):

    def setUp(self):
        # Mock the pynput library so that our unit tests can be run on a headless system
        key_patch = patch('pynput.keyboard.Key')
        self.m_key = key_patch.start()
        self.addCleanup(key_patch.stop)
