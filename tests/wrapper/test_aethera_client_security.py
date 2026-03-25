import sys
from unittest.mock import MagicMock

# Mock requests before importing the client
mock_requests = MagicMock()
sys.modules["requests"] = mock_requests

import unittest
from wrapper.integrations.whatsapp.aethera_client import AetheraWhatsAppClient

class TestAetheraWhatsAppClientSecurity(unittest.TestCase):
    def setUp(self):
        self.client = AetheraWhatsAppClient()

    def test_is_connected_catches_exception(self):
        # Mock session.get to raise a standard Exception
        self.client.session.get.side_effect = Exception("Standard error")

        # Should return False instead of crashing
        result = self.client.is_connected()
        self.assertFalse(result)

    def test_is_connected_does_not_catch_base_exception(self):
        # Mock session.get to raise a BaseException (like KeyboardInterrupt)
        # This test will FAIL before the fix and PASS after the fix
        self.client.session.get.side_effect = KeyboardInterrupt()

        # Should NOT catch KeyboardInterrupt (bare except: would catch it)
        with self.assertRaises(KeyboardInterrupt):
            self.client.is_connected()

if __name__ == "__main__":
    unittest.main()
