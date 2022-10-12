"""Tests for the main module"""

import unittest


class TestMain:
    def test_shorten_new(self, client):
        url = "https://www.clementfleury.me"

        response = client.post("/", params={"url": url})
        assert response.status_code == 200

        actual_short = response.json()
        assert actual_short["url"] == url

    def test_shorten_bad_url(self, client):
        url = "fleuryc"

        response = client.post("/", params={"url": url})
        assert response.status_code == 422

        actual_json = response.json()
        expected_json = {
            "detail": [
                {
                    "loc": ["query", "url"],
                    "msg": "invalid or missing URL scheme",
                    "type": "value_error.url.scheme",
                }
            ]
        }
        assert actual_json == expected_json

    def test_shorten_existing(self, client):
        url = "https://www.clementfleury.me"

        first_response = client.post("/", params={"url": url})
        assert first_response.status_code == 200
        first_short = first_response.json()

        second_response = client.post("/", params={"url": url})
        assert second_response.status_code == 200
        second_short = second_response.json()

        assert first_short == second_short

    def test_shorten_and_get_url(self, client):
        url = "https://www.clementfleury.me"

        first_response = client.post("/", params={"url": url})
        assert first_response.status_code == 200
        first_short = first_response.json()

        key = first_short["key"]
        second_response = client.get(f"/{key}")
        assert second_response.status_code == 200
        second_short = second_response.json()

        assert first_short == second_short

    def test_get_url_not_found(self, client):
        key = "fleuryc"
        response = client.get(f"/{key}")
        assert response.status_code == 404

        actual_response = response.json()
        expected_response = {"detail": "Short not found"}
        assert actual_response == expected_response


if __name__ == "__main__":
    unittest.main()
