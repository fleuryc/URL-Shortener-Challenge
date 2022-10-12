"""Tests for the crud module"""

import unittest

from sqlalchemy.exc import IntegrityError

from src import crud, models, schemas


class TestCrud:
    def test_create_short(self, session):
        short_data = {
            "key": "fleuryc",
            "url": "https://www.clementfleury.me",
        }
        short = schemas.Short(**short_data)
        actual_db_short = crud.create_short(session, short=short)
        expected_db_short = models.Short(**short_data)
        assert actual_db_short == expected_db_short

    def test_create_same_short(self, session):
        short_data = {
            "key": "fleuryc",
            "url": "https://www.clementfleury.me",
        }
        short = schemas.Short(**short_data)
        crud.create_short(session, short=short)
        with unittest.TestCase.assertRaises(self, IntegrityError):
            crud.create_short(session, short=short)


if __name__ == "__main__":
    unittest.main()
