import sys
import unittest
from unittest.mock import MagicMock

# Mock requests module before importing AetheraWhatsAppClient
# This is necessary because the environment lacks the requests library
mock_requests = MagicMock()
sys.modules["requests"] = mock_requests

from wrapper.integrations.whatsapp.aethera_client import AetheraWhatsAppClient

class TestAetheraWhatsAppClient(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:3000/api"
        # Since requests is mocked, AetheraWhatsAppClient(self.base_url)
        # will have a MagicMock as self.session
        self.client = AetheraWhatsAppClient(self.base_url)
        # Mock the session's post method explicitly for clarity,
        # though it's already a MagicMock
        self.client.session.post = MagicMock()

    def test_export_contacts_to_json_success(self):
        # Setup mock response for success (HTTP 200)
        mock_response = MagicMock()
        mock_response.status_code = 200
        expected_data = {"file": "contacts_123456789.json", "count": 42}
        mock_response.json.return_value = {"data": expected_data}
        self.client.session.post.return_value = mock_response

        # Execute the method under test
        result = self.client.export_contacts_to_json()

        # Verify the call and result
        self.client.session.post.assert_called_once_with(f"{self.base_url}/contacts/export/json")
        self.assertEqual(result, expected_data)

    def test_export_contacts_to_json_failure(self):
        # Setup mock response for failure (e.g., HTTP 500)
        mock_response = MagicMock()
        mock_response.status_code = 500
        error_message = "Database connection error"
        mock_response.json.return_value = {"error": error_message}
        self.client.session.post.return_value = mock_response

        # Execute and Verify that it raises an Exception with the error message
        with self.assertRaises(Exception) as cm:
            self.client.export_contacts_to_json()

        self.assertIn(f"Failed to export contacts: {error_message}", str(cm.exception))
        self.client.session.post.assert_called_once_with(f"{self.base_url}/contacts/export/json")

if __name__ == "__main__":
    unittest.main()
