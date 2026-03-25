"""
Aethera WhatsApp Integration Client
Provides a Pythonic interface to interact with the WhatsApp REST API
"""

import requests
from typing import List, Dict, Optional
import time


class AetheraWhatsAppClient:
    """Client for interacting with Aethera WhatsApp REST API"""
    
    def __init__(self, base_url: str = "http://localhost:3000/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    # ========================================================================
    # STATUS METHODS
    # ========================================================================
    
    def is_connected(self) -> bool:
        """Check if WhatsApp client is connected"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200 and response.json()["status"] == "connected"
        except Exception:
            return False
    
    def get_status(self) -> Dict:
        """Get full connection status"""
        response = self.session.get(f"{self.base_url}/status")
        return response.json()
    
    def wait_for_connection(self, timeout: int = 30) -> bool:
        """Wait for WhatsApp to connect, with timeout in seconds"""
        start = time.time()
        while time.time() - start < timeout:
            if self.is_connected():
                return True
            time.sleep(0.5)
        return False
    
    # ========================================================================
    # CHAT METHODS
    # ========================================================================
    
    def get_all_chats(self) -> List[Dict]:
        """Get list of all chats"""
        response = self.session.get(f"{self.base_url}/chats")
        return response.json().get("data", [])
    
    def get_chat(self, chat_id: str) -> Dict:
        """Get specific chat information"""
        response = self.session.get(f"{self.base_url}/chats/{chat_id}")
        return response.json().get("data", {})
    
    def search_chats(self, query: str) -> List[Dict]:
        """Search chats by name or ID"""
        response = self.session.get(f"{self.base_url}/chats/search/{query}")
        return response.json().get("data", [])
    
    def get_unread_chats(self) -> List[Dict]:
        """Get all chats with unread messages"""
        chats = self.get_all_chats()
        return [chat for chat in chats if chat.get("unreadCount", 0) > 0]
    
    # ========================================================================
    # MESSAGE METHODS
    # ========================================================================
    
    def get_messages(self, chat_id: str, limit: int = 50) -> List[Dict]:
        """Get message history from a chat"""
        response = self.session.get(
            f"{self.base_url}/messages/{chat_id}",
            params={"limit": min(limit, 200)}
        )
        return response.json().get("data", [])
    
    def send_message(self, chat_id: str, message: str) -> Dict:
        """Send a message to a chat"""
        response = self.session.post(
            f"{self.base_url}/messages/send",
            json={"chatId": chat_id, "message": message}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to send message: {response.json().get('error')}")
        return response.json().get("data", {})
    
    def send_message_delayed(self, chat_id: str, message: str, delay_ms: int = 1000) -> Dict:
        """Send a message with delay (for rate limiting)"""
        response = self.session.post(
            f"{self.base_url}/messages/send-delayed",
            json={"chatId": chat_id, "message": message, "delayMs": delay_ms}
        )
        return response.json().get("data", {})
    
    def reply_to_message(self, chat_id: str, message_id: str, reply_text: str) -> Dict:
        """Reply to a specific message"""
        response = self.session.post(
            f"{self.base_url}/messages/reply",
            json={"chatId": chat_id, "messageId": message_id, "replyText": reply_text}
        )
        return response.json().get("data", {})
    
    def react_to_message(self, chat_id: str, message_id: str, emoji: str) -> Dict:
        """Add emoji reaction to a message"""
        response = self.session.post(
            f"{self.base_url}/messages/react",
            json={"chatId": chat_id, "messageId": message_id, "emoji": emoji}
        )
        return response.json().get("data", {})
    
    def get_unread_messages(self) -> List[Dict]:
        """Get list of chats with unread messages"""
        response = self.session.get(f"{self.base_url}/messages/unread/list")
        return response.json().get("data", [])
    
    # ========================================================================
    # CONTACT METHODS
    # ========================================================================
    
    def get_contact(self, contact_id: str) -> Dict:
        """Get contact information"""
        response = self.session.get(f"{self.base_url}/contacts/{contact_id}")
        return response.json().get("data", {})
    
    def get_all_contacts(self) -> List[Dict]:
        """Get all contacts as a list"""
        response = self.session.get(f"{self.base_url}/contacts")
        return response.json().get("data", [])
    
    def get_contacts_summary(self) -> Dict:
        """Get contacts with metadata (count, timestamp)"""
        response = self.session.get(f"{self.base_url}/contacts")
        return response.json()
    
    def export_contacts_to_json(self) -> Dict:
        """Export all contacts to JSON file in data folder"""
        response = self.session.post(f"{self.base_url}/contacts/export/json")
        if response.status_code != 200:
            raise Exception(f"Failed to export contacts: {response.json().get('error')}")
        return response.json().get("data", {})
    
    def get_latest_contacts_export(self) -> Dict:
        """Get the latest exported contacts JSON file"""
        response = self.session.get(f"{self.base_url}/contacts/data/latest")
        return response.json().get("data", {})
    
    def list_contacts_exports(self) -> List[Dict]:
        """List all exported contact files"""
        response = self.session.get(f"{self.base_url}/contacts/data/list")
        return response.json().get("data", [])
    
    # ========================================================================
    # GROUP METHODS
    # ========================================================================
    
    def get_all_groups(self) -> List[Dict]:
        """Get list of all groups"""
        response = self.session.get(f"{self.base_url}/groups")
        return response.json().get("data", [])
    
    def get_group(self, group_id: str) -> Dict:
        """Get group information and participants"""
        response = self.session.get(f"{self.base_url}/groups/{group_id}")
        return response.json().get("data", {})
    
    # ========================================================================
    # MEDIA METHODS
    # ========================================================================
    
    def download_media(self, chat_id: str, message_id: str) -> Optional[Dict]:
        """Download media from a message"""
        response = self.session.post(
            f"{self.base_url}/media/download",
            json={"chatId": chat_id, "messageId": message_id}
        )
        return response.json().get("data", {}) if response.status_code == 200 else None


# ============================================================================
# UTILITY FUNCTIONS FOR AETHERA INTEGRATION
# ============================================================================

def get_client(base_url: str = "http://localhost:3000/api") -> AetheraWhatsAppClient:
    """Factory function to get WhatsApp client instance"""
    return AetheraWhatsAppClient(base_url)


if __name__ == "__main__":
    # Example usage
    client = get_client()
    
    # Wait for connection
    if client.wait_for_connection():
        print("✓ Connected to WhatsApp")
        
        # Get all chats
        chats = client.get_all_chats()
        print(f"Found {len(chats)} chats")
        
        # Send a message
        if chats:
            result = client.send_message(chats[0]["id"], "Hello from Aethera!")
            print(f"Message sent: {result}")
    else:
        print("✗ Failed to connect")
