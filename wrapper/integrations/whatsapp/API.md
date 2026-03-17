# Aethera WhatsApp REST API Documentation

**Base URL:** `http://localhost:3000/api`

## Health & Status

### Get Connection Status
```
GET /status
```
**Response:**
```json
{
  "isConnected": true,
  "lastMessage": "12488051142@c.us: Hello",
  "qrCodeStr": ""
}
```

### Get Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "connected",
  "timestamp": "2026-03-16T10:30:00Z"
}
```

---

## Chat Management

### Get All Chats
```
GET /chats
```
**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "12488051142@c.us",
      "name": "Yee",
      "unreadCount": 0,
      "timestamp": 1710591000000,
      "isGroup": false,
      "isPinned": false
    }
  ]
}
```

### Get Specific Chat Info
```
GET /chats/{chatId}
```
**Example:** `GET /chats/12488051142@c.us`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "12488051142@c.us",
    "name": "Yee",
    "isGroup": false,
    "unreadCount": 0,
    "timestamp": 1710591000000,
    "archived": false,
    "pinned": false
  }
}
```

### Search Chats
```
GET /chats/search/{query}
```
**Example:** `GET /chats/search/Yee`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "12488051142@c.us",
      "name": "Yee",
      "isGroup": false
    }
  ]
}
```

---

## Messages

### Get Chat History/Messages
```
GET /messages/{chatId}?limit=50
```
**Query Parameters:**
- `limit` (optional): Number of messages to fetch (default: 50, max: 200)

**Example:** `GET /messages/12488051142@c.us?limit=100`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "from": "12488051142@c.us",
      "to": "120398402934@c.us",
      "body": "Hey, how are you?",
      "timestamp": 1710591000000,
      "hasMedia": false,
      "isForwarded": false
    }
  ]
}
```

### Get Unread Messages
```
GET /messages/unread/list
```
**Response:**
```json
{
  "success": true,
  "data": [
    {
      "chatId": "12488051142@c.us",
      "chatName": "Yee",
      "unreadCount": 3
    }
  ]
}
```

### Send a Message
```
POST /messages/send
Content-Type: application/json

{
  "chatId": "12488051142@c.us",
  "message": "Hello! How are you?"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "messageId": "wamid.xxx",
    "timestamp": 1710591000000
  }
}
```

### Send Message with Delay
```
POST /messages/send-delayed
Content-Type: application/json

{
  "chatId": "12488051142@c.us",
  "message": "Hello!",
  "delayMs": 3000
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "scheduled": true,
    "delayMs": 3000
  }
}
```

### Reply to a Message
```
POST /messages/reply
Content-Type: application/json

{
  "chatId": "12488051142@c.us",
  "messageId": "msg_id_123",
  "replyText": "Thanks for that!"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "replied": true
  }
}
```

### React to a Message
```
POST /messages/react
Content-Type: application/json

{
  "chatId": "12488051142@c.us",
  "messageId": "msg_id_123",
  "emoji": "👍"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "reacted": true,
    "emoji": "👍"
  }
---

## Contacts

### Get All Contacts
```
GET /contacts
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "12488051142@c.us",
      "name": "Yee",
      "number": "1248805114",
      "isMe": false,
      "isUser": true,
      "isContact": true
    },
    {
      "id": "12488054935@c.us",
      "name": "Broo",
      "number": "1248805493",
      "isMe": false,
      "isUser": true,
      "isContact": true
    }
  ],
  "count": 2,
  "timestamp": "2026-03-16T10:30:00Z"
}
```

### Get Contact Info
```
GET /contacts/{contactId}
```
**Example:** `GET /contacts/12488051142@c.us`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "12488051142@c.us",
    "name": "Yee",
    "number": "1248805114",
    "isMe": false,
    "isUser": true,
    "isContact": true
  }
}
```

### Export All Contacts to JSON
```
POST /contacts/export/json
```

**Response:**
```json
{
  "success": true,
  "data": {
    "filename": "contacts_2026-03-16T10-30-00-000Z.json",
    "filepath": "/data/contacts_2026-03-16T10-30-00-000Z.json",
    "contactCount": 15,
    "message": "Contacts exported successfully"
  }
}
```

**Exported file format (data/contacts_*.json):**
```json
{
  "exportedAt": "2026-03-16T10:30:00.000Z",
  "totalContacts": 2,
  "contacts": [
    {
      "id": "12488051142@c.us",
      "name": "Yee",
      "number": "1248805114",
      "isMe": false,
      "isUser": true,
      "isContact": true
    }
  ]
}
```

### Get Latest Exported Contacts
```
GET /contacts/data/latest
```

**Response:**
```json
{
  "success": true,
  "data": {
    "exportedAt": "2026-03-16T10:30:00.000Z",
    "totalContacts": 2,
    "contacts": [...]
  },
  "filename": "contacts_2026-03-16T10-30-00-000Z.json"
}
```

### List All Exported Contact Files
```
GET /contacts/data/list
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "filename": "contacts_2026-03-16T10-30-00-000Z.json",
      "filepath": "/data/contacts_2026-03-16T10-30-00-000Z.json"
    }
  ],
  "count": 1
}
```

---

## Groups

### Get All Groups
```
GET /groups
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "120398402934-1234567890@g.us",
      "name": "Coding Team",
      "participantCount": 5
    }
  ]
}
```

### Get Group Info
```
GET /groups/{groupId}
```
**Example:** `GET /groups/120398402934-1234567890@g.us`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "120398402934-1234567890@g.us",
    "name": "Coding Team",
    "isGroup": true,
    "participantCount": 5,
    "participants": [
      {
        "id": "12488051142@c.us",
        "name": "Yee"
      }
    ]
  }
}
```

---

## Media

### Download Media from Message
```
POST /media/download
Content-Type: application/json

{
  "chatId": "12488051142@c.us",
  "messageId": "msg_id_123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "mimetype": "image/jpeg",
    "data": "base64encodeddata...",
    "filename": "photo.jpg"
  }
}
```

---

## Error Responses

### Connection Not Ready
**Status Code:** 503
```json
{
  "error": "Client not connected"
}
```

### Bad Request
**Status Code:** 400
```json
{
  "error": "Missing chatId or message"
}
```

### Not Found
**Status Code:** 404
```json
{
  "error": "Message not found"
}
```

### Server Error
**Status Code:** 500
```json
{
  "error": "Error message details"
}
```

---

## Usage Examples

### Python (with Aethera)
```python
import requests

BASE_URL = "http://localhost:3000/api"

# Get all chats
response = requests.get(f"{BASE_URL}/chats")
chats = response.json()["data"]

# Send a message
requests.post(f"{BASE_URL}/messages/send", json={
    "chatId": chats[0]["id"],
    "message": "Hello from Aethera!"
})

# Get chat history
messages = requests.get(f"{BASE_URL}/messages/{chats[0]['id']}").json()["data"]

# Get all contacts
contacts = requests.get(f"{BASE_URL}/contacts").json()["data"]
print(f"Total contacts: {len(contacts)}")

# Export contacts to JSON file in data folder
export_result = requests.post(f"{BASE_URL}/contacts/export/json").json()
print(f"Exported to: {export_result['data']['filename']}")

# Get latest exported contacts
latest = requests.get(f"{BASE_URL}/contacts/data/latest").json()
print(f"Loaded {latest['data']['totalContacts']} contacts from export")
```

### JavaScript / Node.js
```javascript
const BASE_URL = "http://localhost:3000/api";

// Get all chats
const response = await fetch(`${BASE_URL}/chats`);
const { data: chats } = await response.json();

// Send message
await fetch(`${BASE_URL}/messages/send`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    chatId: chats[0].id,
    message: "Hello from Aethera!"
  })
});
```

### cURL
```bash
# Get status
curl http://localhost:3000/api/status

# Get all chats
curl http://localhost:3000/api/chats

# Get all contacts
curl http://localhost:3000/api/contacts

# Export contacts to JSON file in data folder
curl -X POST http://localhost:3000/api/contacts/export/json

# Get latest exported contacts
curl http://localhost:3000/api/contacts/data/latest

# List all exported contact files
curl http://localhost:3000/api/contacts/data/list

# Send message
curl -X POST http://localhost:3000/api/messages/send \
  -H "Content-Type: application/json" \
  -d '{"chatId": "12488051142@c.us", "message": "Hello!"}'
```

---

## Rate Limiting & Best Practices

1. **Connection Check**: Always verify `/health` or `/status` before operations
2. **Delays**: Use `/messages/send-delayed` for bulk messaging (rate limiting)
3. **Caching**: Cache chat lists for faster UI responses
4. **Message Limits**: Don't fetch more than 200 messages at a time
5. **Error Handling**: Always handle 503 (Service Unavailable) responses

---

## Notes

- All timestamps are in milliseconds since epoch
- Chat IDs follow format: `<phoneNumber>@c.us` for individuals, `<groupId>@g.us` for groups
- Emoji reactions should be single character emojis only
- Media download returns base64 encoded data
