"""Tests for the utils module"""

import unittest
from random import randrange

from src.utils import generate_key


class TestUtils(unittest.TestCase):
    def test_generate_key_no_parameter(self):
        actual_key = generate_key()
        expected_key_regex = r"^[a-zA-Z0-9]{5}$"
        self.assertRegex(actual_key, expected_key_regex)

    def test_generate_key_10(self):
        size = 10
        actual_key = generate_key(size)
        expected_key_regex = rf"^[a-zA-Z0-9]{{{size}}}$"
        self.assertRegex(actual_key, expected_key_regex)

    def test_generate_key_random_size(self):
        size = randrange(2, 100)
        actual_key = generate_key(size)
        expected_key_regex = rf"^[a-zA-Z0-9]{{{size}}}$"
        self.assertRegex(actual_key, expected_key_regex)

    def test_generate_key_zero(self):
        actual_key = generate_key(0)
        assert actual_key == ""

    def test_generate_key_negative(self):
        actual_key = generate_key(-1)
        assert actual_key == ""
