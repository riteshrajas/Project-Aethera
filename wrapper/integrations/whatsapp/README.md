# WhatsApp Integration (Baileys)

This folder contains a minimal scaffold to connect Project Aethera to WhatsApp using Baileys.

Quick start

1. Install dependencies:

```bash
cd wrapper/integrations/whatsapp
npm install @adiwajshing/baileys
```

2. Run the client:

```bash
npm start
```

Notes
- The example uses Baileys and stores auth state in `auth_info.json` (single-file auth). The first run will prompt you to scan a QR code in the console.
- To integrate with a Beeper/MCP server, implement `sendToMCP()` in `index.js` to forward messages via HTTP/WebSocket and receive commands to perform actions (auto-reply toggles, templates, etc.).
- Be careful with privacy and permissions — only connect accounts you control.

Next steps I can do for you

- Add a `sendToMCP()` implementation and example config for Beeper MCP.
- Add an express endpoint to receive commands from the MCP server and trigger replies.
