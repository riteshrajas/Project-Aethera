const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');

// Express REST API setup
const app = express();
app.use(express.json());
const DASHPORT = process.env.AETHERA_WHATSAPP_PORT || 3000;

let lastMessage = null;
let isConnected = false;
let qrCodeStr = "";
let messageCache = [];

app.get('/dashboard', (req, res) => {
  res.sendFile(__dirname + '/dashboard.html');
});

// ============================================================================
// HEALTH & STATUS ENDPOINTS
// ============================================================================

app.get('/api/status', (req, res) => {
  res.json({
    isConnected,
    lastMessage,
    qrCodeStr
  });
});

app.get('/api/health', (req, res) => {
  res.json({
    status: isConnected ? 'connected' : 'disconnected',
    timestamp: new Date().toISOString()
  });
});

// ============================================================================
// CHAT MANAGEMENT ENDPOINTS
// ============================================================================

// Get all chats
app.get('/api/chats', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  try {
      const chats = await client.getChats();
      const chatList = chats.map(c => ({
          id: c.id._serialized,
          name: c.name || c.id.user,
          unreadCount: c.unreadCount,
          timestamp: c.timestamp,
          isGroup: c.isGroup,
          isPinned: c.isPinned || false
      }));
      res.json({ success: true, data: chatList });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// Get specific chat info
app.get('/api/chats/:chatId', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  try {
      const chat = await client.getChatById(decodeURIComponent(req.params.chatId));
      res.json({
          success: true,
          data: {
              id: chat.id._serialized,
              name: chat.name || chat.id.user,
              isGroup: chat.isGroup,
              unreadCount: chat.unreadCount,
              timestamp: chat.timestamp,
              archived: chat.archived || false,
              pinned: chat.isPinned || false
          }
      });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// Search chats by name or ID
app.get('/api/chats/search/:query', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  try {
      const allChats = await client.getChats();
      const query = decodeURIComponent(req.params.query).toLowerCase();
      const results = allChats.filter(c => 
          (c.name && c.name.toLowerCase().includes(query)) || 
          c.id.user.toLowerCase().includes(query)
      );
      const chatList = results.map(c => ({
          id: c.id._serialized,
          name: c.name || c.id.user,
          isGroup: c.isGroup
      }));
      res.json({ success: true, data: chatList });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// ============================================================================
// MESSAGE ENDPOINTS
// ============================================================================

// Get chat history/messages
app.get('/api/messages/:chatId', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  
  const limit = Math.min(parseInt(req.query.limit) || 50, 200);
  
  try {
      const chat = await client.getChatById(decodeURIComponent(req.params.chatId));
      const messages = await chat.fetchMessages({ limit });

      const messageHistory = messages.map(msg => ({
          from: msg.from,
          to: msg.to,
          body: msg.body,
          timestamp: msg.timestamp,
          hasMedia: msg.hasMedia,
          isForwarded: msg.isForwarded
      }));

      res.json({ success: true, data: messageHistory });
  } catch (error) {
      res.status(500).json({ error: error.toString() });
  }
});

// Get unread messages
app.get('/api/messages/unread/list', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  try {
      const chats = await client.getChats();
      const unreadChats = chats.filter(c => c.unreadCount > 0);
      
      const unreadData = unreadChats.map(c => ({
          chatId: c.id._serialized,
          chatName: c.name || c.id.user,
          unreadCount: c.unreadCount
      }));
      
      res.json({ success: true, data: unreadData });
  } catch (error) {
      res.status(500).json({ error: error.toString() });
  }
});

// Send a message
app.post('/api/messages/send', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  
  const { chatId, message } = req.body;
  if (!chatId || !message) {
      return res.status(400).json({ error: 'Missing chatId or message' });
  }

  try {
      const result = await client.sendMessage(chatId, message);
      res.json({ success: true, data: { messageId: result.id, timestamp: result.timestamp } });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// Send message with delay (for rate limiting)
app.post('/api/messages/send-delayed', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  
  const { chatId, message, delayMs } = req.body;
  if (!chatId || !message) {
      return res.status(400).json({ error: 'Missing chatId or message' });
  }
  
  const delay = Math.min(delayMs || 1000, 10000);

  try {
      setTimeout(async () => {
          await client.sendMessage(chatId, message);
      }, delay);
      
      res.json({ success: true, data: { scheduled: true, delayMs: delay } });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// Reply to a message (via message ID)
app.post('/api/messages/reply', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  
  const { chatId, messageId, replyText } = req.body;
  if (!chatId || !messageId || !replyText) {
      return res.status(400).json({ error: 'Missing chatId, messageId, or replyText' });
  }

  try {
      const chat = await client.getChatById(chatId);
      const messages = await chat.fetchMessages({ limit: 200 });
      const targetMsg = messages.find(m => m.id.id === messageId);
      
      if (!targetMsg) {
          return res.status(404).json({ error: 'Message not found' });
      }
      
      await targetMsg.reply(replyText);
      res.json({ success: true, data: { replied: true } });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// React to a message
app.post('/api/messages/react', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  
  const { chatId, messageId, emoji } = req.body;
  if (!chatId || !messageId || !emoji) {
      return res.status(400).json({ error: 'Missing chatId, messageId, or emoji' });
  }

  try {
      const chat = await client.getChatById(chatId);
      const messages = await chat.fetchMessages({ limit: 200 });
      const targetMsg = messages.find(m => m.id.id === messageId);
      
      if (!targetMsg) {
          return res.status(404).json({ error: 'Message not found' });
      }
      
      await targetMsg.react(emoji);
      res.json({ success: true, data: { reacted: true, emoji } });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// ============================================================================
// CONTACT ENDPOINTS
// ============================================================================

// Get contact info
app.get('/api/contacts/:contactId', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  
  try {
      const contact = await client.getContactById(decodeURIComponent(req.params.contactId));
      res.json({
          success: true,
          data: {
              id: contact.id._serialized,
              name: contact.name,
              number: contact.number,
              isMe: contact.isMe,
              isUser: contact.isUser,
              isContact: contact.isContact
          }
      });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// Get all contacts
app.get('/api/contacts', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  
  try {
      const contacts = await client.getContacts();
      const contactList = contacts.map(c => ({
          id: c.id._serialized,
          name: c.name || 'Unknown',
          number: c.number || 'N/A',
          isMe: c.isMe,
          isUser: c.isUser,
          isContact: c.isContact
      }));
      
      res.json({
          success: true,
          data: contactList,
          count: contactList.length,
          timestamp: new Date().toISOString()
      });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// Export all contacts to JSON file
app.post('/api/contacts/export/json', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  
  const fs = require('fs');
  const path = require('path');
  
  try {
      const contacts = await client.getContacts();
      const contactList = contacts.map(c => ({
          id: c.id._serialized,
          name: c.name || 'Unknown',
          number: c.number || 'N/A',
          isMe: c.isMe,
          isUser: c.isUser,
          isContact: c.isContact
      }));
      
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const filename = `contacts_${timestamp}.json`;
      const dataDir = path.join(__dirname, '../../..', 'data');
      const filepath = path.join(dataDir, filename);
      
      // Ensure data directory exists
      if (!fs.existsSync(dataDir)) {
          fs.mkdirSync(dataDir, { recursive: true });
      }
      
      const exportData = {
          exportedAt: new Date().toISOString(),
          totalContacts: contactList.length,
          contacts: contactList
      };
      
      fs.writeFileSync(filepath, JSON.stringify(exportData, null, 2));
      
      res.json({
          success: true,
          data: {
              filename,
              filepath,
              contactCount: contactList.length,
              message: 'Contacts exported successfully'
          }
      });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// Get latest exported contacts JSON from data folder
app.get('/api/contacts/data/latest', async (req, res) => {
  const fs = require('fs');
  const path = require('path');
  
  try {
      const dataDir = path.join(__dirname, '../../..', 'data');
      
      if (!fs.existsSync(dataDir)) {
          return res.status(404).json({ error: 'Data folder not found' });
      }
      
      const files = fs.readdirSync(dataDir)
          .filter(f => f.startsWith('contacts_') && f.endsWith('.json'))
          .sort()
          .reverse();
      
      if (files.length === 0) {
          return res.status(404).json({ error: 'No exported contacts found' });
      }
      
      const latestFile = files[0];
      const filepath = path.join(dataDir, latestFile);
      const data = JSON.parse(fs.readFileSync(filepath, 'utf8'));
      
      res.json({
          success: true,
          data,
          filename: latestFile
      });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// List all exported contact files
app.get('/api/contacts/data/list', async (req, res) => {
  const fs = require('fs');
  const path = require('path');
  
  try {
      const dataDir = path.join(__dirname, '../../..', 'data');
      
      if (!fs.existsSync(dataDir)) {
          return res.json({ success: true, data: [] });
      }
      
      const files = fs.readdirSync(dataDir)
          .filter(f => f.startsWith('contacts_') && f.endsWith('.json'))
          .map(f => ({
              filename: f,
              filepath: path.join(dataDir, f)
          }))
          .sort((a, b) => b.filename.localeCompare(a.filename));
      
      res.json({
          success: true,
          data: files,
          count: files.length
      });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// ============================================================================
// GROUP ENDPOINTS
// ============================================================================

// Get group info
app.get('/api/groups/:groupId', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  
  try {
      const chat = await client.getChatById(decodeURIComponent(req.params.groupId));
      if (!chat.isGroup) {
          return res.status(400).json({ error: 'Chat is not a group' });
      }
      
      const participants = chat.participants.map(p => ({
          id: p.id._serialized,
          name: p.name
      }));
      
      res.json({
          success: true,
          data: {
              id: chat.id._serialized,
              name: chat.name,
              isGroup: true,
              participantCount: chat.participants.length,
              participants
          }
      });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// List all groups
app.get('/api/groups', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  try {
      const chats = await client.getChats();
      const groups = chats.filter(c => c.isGroup).map(c => ({
          id: c.id._serialized,
          name: c.name,
          participantCount: c.participants?.length || 0
      }));
      res.json({ success: true, data: groups });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// ============================================================================
// MEDIA ENDPOINTS
// ============================================================================

// Download media from message
app.post('/api/media/download', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  
  const { chatId, messageId } = req.body;
  if (!chatId || !messageId) {
      return res.status(400).json({ error: 'Missing chatId or messageId' });
  }

  try {
      const chat = await client.getChatById(chatId);
      const messages = await chat.fetchMessages({ limit: 200 });
      const targetMsg = messages.find(m => m.id.id === messageId);
      
      if (!targetMsg || !targetMsg.hasMedia) {
          return res.status(404).json({ error: 'Message or media not found' });
      }
      
      const media = await targetMsg.downloadMedia();
      res.json({
          success: true,
          data: {
              mimetype: media.mimetype,
              data: media.data,
              filename: media.filename
          }
      });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

// ============================================================================
// OLD COMPATIBILITY ENDPOINTS (DEPRECATED)
// ============================================================================

app.get('/api/chats', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Client not connected' });
  try {
      const chats = await client.getChats();
      const chatList = chats.map(c => ({
          id: c.id._serialized,
          name: c.name || c.id.user,
          unreadCount: c.unreadCount,
          timestamp: c.timestamp,
          isGroup: c.isGroup
      }));
      res.json(chatList);
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

app.post('/api/send-message', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Not connected' });
  
  const { chatId, message } = req.body;
  if (!chatId || !message) return res.status(400).json({ error: 'Missing chatId or message' });

  try {
      await client.sendMessage(chatId, message);
      res.json({ success: true });
  } catch (err) {
      res.status(500).json({ error: err.toString() });
  }
});

app.get('/contact-history/:contactId', async (req, res) => {
  if (!isConnected) return res.status(503).json({ error: 'Not connected' });
  const contactId = req.params.contactId;

  try {
      const chat = await client.getChatById(contactId);
      const messages = await chat.fetchMessages({ limit: 50 });

      const messageHistory = messages.map(msg => ({
          from: msg.from,
          body: msg.body,
          timestamp: msg.timestamp
      }));

      res.json({ contactId, history: messageHistory });
  } catch (error) {
      res.status(500).json({ error: 'Failed to fetch contact history' });
  }
});

app.get('/profile', (req, res) => {
    res.sendFile(__dirname + '/profile.html');
});

// ============================================================================
// SERVER INITIALIZATION
// ============================================================================

const server = app.listen(DASHPORT, () => {
  console.log(`Aethera WhatsApp REST API running at http://localhost:${DASHPORT}`);
  console.log(`Dashboard available at http://localhost:${DASHPORT}/dashboard`);
  console.log(`API Documentation: http://localhost:${DASHPORT}/api/docs`);
}).on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.log(`Port ${DASHPORT} already in use. Try setting AETHERA_WHATSAPP_PORT environment variable.`);
  }
});

// ============================================================================
// WHATSAPP CLIENT INITIALIZATION
// ============================================================================

const client = new Client({
    authStrategy: new LocalAuth({ dataPath: './auth_data' }),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-extensions']
    }
});

client.on('qr', (qr) => {
    console.log('QR Code generated. Scan with WhatsApp → Linked Devices');
    qrcode.generate(qr, {small: true}, (qrcodeStr) => {
        qrCodeStr = qrcodeStr;
        console.log(qrcodeStr);
    });
});

client.on('ready', () => {
    isConnected = true;
    qrCodeStr = "";
    console.log('✓ WhatsApp client connected and ready');
});

client.on('message', async (msg) => {
    lastMessage = `${msg.from}: ${msg.body}`;
    messageCache.push({
        from: msg.from,
        body: msg.body,
        timestamp: new Date().toISOString()
    });
    // Keep cache size limited
    if (messageCache.length > 100) {
        messageCache = messageCache.slice(-100);
    }
    
    console.log('→ Message:', lastMessage);

    // Auto-reply logic
    if (msg.body.toLowerCase() === '!ping') {
        msg.reply('pong from Aethera!');
    }
});

client.on('disconnected', (reason) => {
    console.log('✗ Client disconnected:', reason);
    isConnected = false;
});

client.initialize();

