# 🧩 Agora - Modular AI Agent Chat Platform

> **Brutally simple.** Extremely modular. Production-ready.

Agora is a minimal, open-source chat platform for running AI agent frameworks. Think "ChatGPT, but open and composable."

## ✨ Features

- 🎯 **Modular Agents** - Each agent self-contained with own config, memory, and tools
- 🔄 **Real-time Streaming** - WebSocket-based token streaming for instant responses
- 💾 **Per-Agent Memory** - SQLite-based context management, no token bloat
- 🎨 **Dark Mode UI** - Clean, Raycast-inspired interface
- 🚀 **Production Ready** - FastAPI backend, Next.js frontend, Docker deployment
- 🧪 **No Framework Bloat** - Direct OpenAI API calls, no LangChain/CrewAI overhead

## 🏗️ Architecture

```
┌──────────────────────────────┐
│ FRONTEND (Next.js)           │
│  - Chat UI                   │
│  - WebSocket stream          │
│  - Agent selector             │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ BACKEND (FastAPI)            │
│  - /chat + /agents routes    │
│  - Orchestrator (router)     │
│  - Context manager per agent │
│  - WebSocket streaming       │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ AGENT MODULES                │
│  - paper_writer (academic)   │
│  - shopper (products)        │
│  - [add your own agents]     │
└──────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API key
- Python 3.10+ (for local development)
- Node.js 20+ (for local development)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/agora.git
cd agora
```

2. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. **Start with Docker Compose**

```bash
docker compose up
```

4. **Access the app**

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
agora/
├── backend/
│   ├── main.py                  # FastAPI application
│   ├── routes/
│   │   ├── chat.py              # Chat endpoints
│   │   └── agents.py            # Agent management
│   ├── core/
│   │   ├── orchestrator.py      # Agent routing & execution
│   │   ├── memory.py            # SQLite context management
│   │   └── router.py            # Intent detection
│   ├── agents/
│   │   ├── paper_writer/        # Academic writing agent
│   │   │   ├── agent.py
│   │   │   ├── config.yaml
│   │   │   ├── prompt.txt
│   │   │   └── memory.db
│   │   └── shopper/             # Shopping agent
│   │       ├── agent.py
│   │       ├── config.yaml
│   │       └── tools.py
│   └── utils/
│       ├── openai_client.py     # OpenAI API wrapper
│       └── logger.py            # Logging utility
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Main chat page
│   │   └── layout.tsx           # Root layout
│   ├── components/
│   │   ├── ChatWindow.tsx       # Message display
│   │   ├── MessageBubble.tsx    # Individual messages
│   │   ├── InputBar.tsx         # Message input
│   │   └── AgentSelector.tsx    # Agent dropdown
│   ├── hooks/
│   │   └── useChat.ts           # Zustand state management
│   └── lib/
│       ├── socket.ts            # WebSocket client
│       └── utils.ts             # Utility functions
│
└── docker-compose.yml           # Docker orchestration
```

## 🤖 Built-in Agents

### Academic Writer (`paper_writer`)

Writes academic-style paragraphs and summaries.

**Usage:**
- Type naturally: "Write about quantum computing"
- Explicit: `/paper_writer explain machine learning`

### Shopper (`shopper`)

Finds product recommendations (mock data for MVP).

**Usage:**
- Type naturally: "Find me a laptop"
- Explicit: `/shopper best headphones under $200`

## 🔧 Adding Your Own Agent

1. **Create agent folder**

```bash
mkdir backend/agents/your_agent
cd backend/agents/your_agent
```

2. **Create `config.yaml`**

```yaml
name: "Your Agent Name"
description: "What your agent does"
model: "gpt-4o-mini"
max_context: 6000
temperature: 0.7
```

3. **Create `agent.py`**

```python
import yaml
from pathlib import Path
from utils.openai_client import llm_call_with_context

class Agent:
    def __init__(self):
        self.name = "your_agent"
        # Load config...

    async def run(self, query, context, stream=False):
        # Your agent logic here
        return await llm_call_with_context(
            query=query,
            context=context,
            model=self.model,
            stream=stream
        )
```

4. **Register in router** (edit `backend/core/router.py`)

```python
self.agent_keywords = {
    "paper_writer": ["write", "academic", "paper"],
    "shopper": ["buy", "shop", "product"],
    "your_agent": ["keyword1", "keyword2"],  # Add this
}
```

5. **Restart and test!**

## 🌐 API Reference

### POST `/chat`

Send a non-streaming chat message.

**Request:**
```json
{
  "query": "Write about AI",
  "session_id": "optional-session-id",
  "agent_name": "paper_writer"
}
```

**Response:**
```json
{
  "response": "AI is a field of...",
  "session_id": "abc123",
  "agent_used": "paper_writer"
}
```

### WebSocket `/chat/ws`

Real-time streaming chat.

**Client sends:**
```json
{
  "query": "Write about AI",
  "agent_name": "paper_writer"
}
```

**Server streams:**
```json
{"type": "start", "session_id": "abc123"}
{"type": "token", "content": "AI"}
{"type": "token", "content": " is"}
{"type": "end", "session_id": "abc123"}
```

### GET `/agents`

List available agents.

**Response:**
```json
{
  "agents": [
    {
      "name": "paper_writer",
      "description": "Writes academic content",
      "model": "gpt-4o-mini"
    }
  ],
  "count": 2
}
```

## 🛠️ Development

### Local Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Local Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Backend tests (coming soon)
cd backend
pytest

# Frontend tests (coming soon)
cd frontend
npm test
```

## 🐳 Deployment

### Production with Docker Compose

```bash
docker compose -f docker-compose.prod.yml up -d
```

### Vercel (Frontend)

```bash
cd frontend
vercel --prod
```

### Fly.io (Backend)

```bash
cd backend
flyctl deploy
```

## 🔐 Environment Variables

### Backend

- `OPENAI_API_KEY` - Your OpenAI API key (required)

### Frontend

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://backend:8000)
- `NEXT_PUBLIC_WS_URL` - WebSocket URL (default: ws://localhost:8000)

## 🧠 Memory & Token Management

- Each agent maintains its own SQLite database
- Stores last 5 message exchanges per session
- Automatically summarizes/deletes old context to prevent token bloat
- No shared global context between agents

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-agent`)
3. Commit your changes (`git commit -m 'Add amazing agent'`)
4. Push to the branch (`git push origin feature/amazing-agent`)
5. Open a Pull Request

## 🎯 Roadmap

- [ ] Agent registry (install agents via CLI)
- [ ] Multi-user support with authentication
- [ ] Persistent sessions across browser restarts
- [ ] Agent marketplace
- [ ] Voice input/output
- [ ] Mobile app
- [ ] Self-hosted LLM support (Ollama, LocalAI)

## 📧 Support

- Issues: [GitHub Issues](https://github.com/yourusername/agora/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/agora/discussions)

## ⭐ Star History

If you find Agora useful, please consider starring the repository!

---

**Built with ❤️ by the open-source community**

*Agora v0.1.0 - "The Minimal MVP"*
