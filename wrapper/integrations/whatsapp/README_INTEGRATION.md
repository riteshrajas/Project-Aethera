# WhatsApp Integration Guide for Aethera Core

This guide shows how to integrate WhatsApp messaging capabilities into Project Aethera's core modules.

## Quick Start

### Import the Client
```python
from wrapper.integrations.whatsapp.aethera_client import get_client

# Get client instance
whatsapp = get_client()

# Wait for connection
if whatsapp.wait_for_connection(timeout=30):
    print("Ready to use WhatsApp")
```

## Common Use Cases

### 1. Send Notifications
```python
whatsapp = get_client()

# Get a specific contact
chats = whatsapp.search_chats("contact_name")
if chats:
    chat_id = chats[0]["id"]
    whatsapp.send_message(chat_id, "Your notification message here")
```

### 2. Process Incoming Messages
```python
def process_messages(whatsapp):
    """Monitor and process incoming messages"""
    unread = whatsapp.get_unread_messages()
    for chat_info in unread:
        chat_id = chat_info["chatId"]
        messages = whatsapp.get_messages(chat_id)
        
        for msg in messages:
            print(f"From {msg['from']}: {msg['body']}")
            # Process message...
```

### 3. Auto-Reply System
```python
def auto_reply_demo(whatsapp):
    """Example auto-reply implementation"""
    chats = whatsapp.get_all_chats()
    
    for chat in chats:
        messages = whatsapp.get_messages(chat["id"], limit=10)
        
        for msg in messages:
            # Example: Reply to messages containing "help"
            if "help" in msg["body"].lower():
                whatsapp.reply_to_message(
                    chat["id"],
                    msg["id"],
                    "Sure! I'm here to help. What do you need?"
                )
```

### 4. Group Management
```python
def analyze_groups(whatsapp):
    """Analyze groups the user is part of"""
    groups = whatsapp.get_all_groups()
    
    for group in groups:
        group_details = whatsapp.get_group(group["id"])
        print(f"Group: {group['name']}")
        print(f"Participants: {group_details['participantCount']}")
        
        # Send group message
        whatsapp.send_message(
            group["id"],
            f"Hello {group['name']} members!"
        )
```

### 5. Contact Management & Export
```python
def manage_contacts(whatsapp):
    """Get all contacts and export to JSON"""
    # Get all contacts
    all_contacts = whatsapp.get_all_contacts()
    print(f"Total contacts: {len(all_contacts)}")
    
    for contact in all_contacts:
        print(f"  - {contact['name']} ({contact['number']})")
    
    # Export contacts to data folder as JSON
    export_result = whatsapp.export_contacts_to_json()
    print(f"Exported to: {export_result['filename']}")
    
    # Later, retrieve the exported data
    latest_export = whatsapp.get_latest_contacts_export()
    print(f"Loaded {latest_export['totalContacts']} contacts from export")
```

### 6. Message Analysis (for core.information_management)
```python
from core.information_management.data_analysis import analyze_text_frequency

def analyze_chat_content(whatsapp, chat_id):
    """Analyze message content in a chat"""
    messages = whatsapp.get_messages(chat_id, limit=200)
    
    # Combine all message bodies
    all_text = " ".join([msg["body"] for msg in messages])
    
    # Use Aethera's text analysis
    stats = analyze_text_frequency(all_text)
    return stats
```

## Module Integration Points

### business_ops/communication.py
```python
from wrapper.integrations.whatsapp.aethera_client import get_client

class WhatsAppCommunication:
    def __init__(self):
        self.whatsapp = get_client()
    
    def send_notification(self, contact_name, message):
        """Send WhatsApp notification"""
        chats = self.whatsapp.search_chats(contact_name)
        if chats:
            return self.whatsapp.send_message(chats[0]["id"], message)
    
    def broadcast_message(self, message):
        """Send message to all contacts"""
        chats = self.whatsapp.get_all_chats()
        for chat in chats:
            self.whatsapp.send_message_delayed(
                chat["id"], 
                message,
                delay_ms=2000  # Rate limit: 2 seconds between messages
            )
```

### business_ops/scheduling.py
```python
from wrapper.integrations.whatsapp.aethera_client import get_client
import schedule
import time

def schedule_whatsapp_messages():
    """Schedule WhatsApp messages using business ops"""
    whatsapp = get_client()
    
    def send_daily_update():
        contacts = whatsapp.search_chats("my_contact")
        if contacts:
            whatsapp.send_message(
                contacts[0]["id"],
                "Daily update: All systems operational"
            )
    
    schedule.every().day.at("09:00").do(send_daily_update)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
```

### information_management/data_analysis.py Integration
```python
def analyze_conversation_pattern(whatsapp, chat_id):
    """Analyze conversation patterns in a chat"""
    messages = whatsapp.get_messages(chat_id, limit=100)
    
    # Extract message bodies
    texts = [msg["body"] for msg in messages]
    
    # Analyze frequency
    from core.information_management.data_analysis import analyze_text_frequency
    stats = analyze_text_frequency(" ".join(texts))
    
    return {
        "chat_id": chat_id,
        "message_count": len(messages),
        "word_frequency": stats
    }
```

## Error Handling

```python
from wrapper.integrations.whatsapp.aethera_client import get_client

whatsapp = get_client()

# Always check connection first
if not whatsapp.is_connected():
    print("WhatsApp not connected. Waiting...")
    if not whatsapp.wait_for_connection():
        raise Exception("Could not establish WhatsApp connection")

try:
    result = whatsapp.send_message(chat_id, message)
    print(f"Successfully sent: {result}")
except Exception as e:
    print(f"Error sending message: {e}")
```

## Rate Limiting & Best Practices

1. **Use delayed sending for bulk operations:**
   ```python
   for contact in contacts:
       whatsapp.send_message_delayed(contact["id"], msg, delay_ms=3000)
   ```

2. **Cache results to reduce API calls:**
   ```python
   chats = whatsapp.get_all_chats()  # Cache this
   unread = whatsapp.get_unread_chats()  # Filter cached result
   ```

3. **Batch operations with proper delays:**
   ```python
   messages = whatsapp.get_messages(chat_id, limit=200)
   for msg in messages:
       process(msg)
       time.sleep(0.5)  # Don't hammer the API
   ```

## Testing

```python
# test_whatsapp_integration.py
from wrapper.integrations.whatsapp.aethera_client import get_client

def test_connection():
    """Test WhatsApp connection"""
    client = get_client()
    assert client.is_connected(), "WhatsApp should be connected"

def test_send_message():
    """Test message sending"""
    client = get_client()
    chats = client.get_all_chats()
    assert len(chats) > 0, "Should have at least one chat"
    
    result = client.send_message(chats[0]["id"], "Test message")
    assert result.get("messageId"), "Should return message ID"

def test_search_chats():
    """Test chat search"""
    client = get_client()
    results = client.search_chats("test")
    assert isinstance(results, list), "Should return list"
```

## Environment Configuration

Set these environment variables in `.env`:

```env
AETHERA_WHATSAPP_PORT=3000
AETHERA_WHATSAPP_API_URL=http://localhost:3000/api
```

Then access in your Aethera modules:

```python
import os

API_URL = os.getenv("AETHERA_WHATSAPP_API_URL", "http://localhost:3000/api")
client = get_client(API_URL)
```
