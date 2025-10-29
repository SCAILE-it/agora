"""
ABOUTME: Main FastAPI application for Agora backend
ABOUTME: Configures CORS, routes, and WebSocket support for agent orchestration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import chat_router, agents_router
from utils.logger import logger

# Initialize FastAPI app
app = FastAPI(
    title="Agora API",
    description="Minimal, modular AI agent chat platform",
    version="0.1.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(chat_router)
app.include_router(agents_router)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Agora API is running",
        "version": "0.1.0",
        "status": "healthy"
    }

@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": "agora-backend",
        "endpoints": {
            "chat": "/chat",
            "websocket": "/chat/ws",
            "agents": "/agents"
        }
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Agora backend server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
