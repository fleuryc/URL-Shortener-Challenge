"""Tests for the main module"""

import sys
import unittest

from fastapi.testclient import TestClient

from src.config import get_settings
from src.main import app

client = TestClient(app)


class TestEnvironment(unittest.TestCase):
    def test_python_version(self):
        actual_python_version = sys.version_info
        expected_minimum_python_version = (
            3,
            10,
        )
        assert actual_python_version >= expected_minimum_python_version

    def test_settings(self):
        actual_settings_keys = list(dict(get_settings()).keys())
        assert "SQLALCHEMY_DATABASE_URL" in actual_settings_keys


class TestMain(unittest.TestCase):
    def test_shorten_url(self):
        url = "https://www.clementfleury.me"

        response = client.post("/", params={"url": url})
        assert response.status_code == 200

        actual_key = response.json()
        expected_key = "fleuryc"
        assert actual_key == expected_key

    def test_get_url(self):
        key = "toto"
        response = client.get(f"/{key}")
        assert response.status_code == 200

        actual_url = response.json()
        expected_url = "https://www.clementfleury.me"
        assert actual_url == expected_url


if __name__ == "__main__":
    unittest.main()
