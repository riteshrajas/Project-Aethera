import unittest

from services.web_client import create_app


class TestWebClient(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_index_get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Project Aethera Web Client", response.data)

    def test_index_post(self):
        response = self.client.post("/", data={"text": "Hello world hello"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"hello", response.data)
        self.assertIn(b"2", response.data)

    def test_index_post_empty(self):
        response = self.client.post("/", data={"text": "   "})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please enter text to analyze.", response.data)


if __name__ == "__main__":
    unittest.main()
