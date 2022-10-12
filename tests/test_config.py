"""Tests for the config module"""

import sys
import unittest

from fastapi.testclient import TestClient

from src.config import get_settings, get_test_settings
from src.main import app

client = TestClient(app)


class TestConfig(unittest.TestCase):
    def test_python_version(self):
        actual_python_version = sys.version_info
        expected_python_version_min = (
            3,
            10,
        )
        assert actual_python_version >= expected_python_version_min

    def test_get_settings(self):
        actual_settings = get_settings()
        assert len(dict(actual_settings)["SQLALCHEMY_DATABASE_URL"]) > 0

    def test_get_test_settings(self):
        actual_settings = get_test_settings()
        assert len(dict(actual_settings)["SQLALCHEMY_DATABASE_URL"]) > 0


if __name__ == "__main__":
    unittest.main()
