"""API routes for chat functionality."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from core.orchestrator import Orchestrator
from utils.logger import logger

router = APIRouter(prefix="/chat", tags=["chat"])
orchestrator = Orchestrator()

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str
    session_id: Optional[str] = None
    agent_name: Optional[str] = None

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    session_id: str
    agent_used: str

@router.post("/")
async def chat(request: ChatRequest):
    """
    Process a chat message (non-streaming).

    Args:
        request: Chat request with query and optional session_id/agent_name

    Returns:
        Agent's response
    """
    session_id = request.session_id or str(uuid.uuid4())

    try:
        response = await orchestrator.handle_query(
            query=request.query,
            session_id=session_id,
            agent_name=request.agent_name,
            stream=False
        )

        return {
            "response": response,
            "session_id": session_id,
            "agent_used": request.agent_name or "auto"
        }

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for streaming chat responses.

    Protocol:
        Client sends: {"query": "...", "session_id": "...", "agent_name": "..."}
        Server streams: {"type": "token", "content": "..."} for each token
        Server ends with: {"type": "end", "session_id": "..."}
    """
    await websocket.accept()
    logger.info("WebSocket connection established")

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            query = data.get("query")
            session_id = data.get("session_id") or str(uuid.uuid4())
            agent_name = data.get("agent_name")

            if not query:
                await websocket.send_json({
                    "type": "error",
                    "content": "No query provided"
                })
                continue

            logger.info(f"Received WebSocket query: {query[:50]}...")

            try:
                # Send start message
                await websocket.send_json({
                    "type": "start",
                    "session_id": session_id,
                    "agent": agent_name or "auto"
                })

                # Stream response
                response_gen = await orchestrator.handle_query(
                    query=query,
                    session_id=session_id,
                    agent_name=agent_name,
                    stream=True
                )

                async for chunk in response_gen:
                    await websocket.send_json({
                        "type": "token",
                        "content": chunk
                    })

                # Send completion message
                await websocket.send_json({
                    "type": "end",
                    "session_id": session_id
                })

            except Exception as e:
                logger.error(f"Error processing query: {e}")
                await websocket.send_json({
                    "type": "error",
                    "content": str(e)
                })

    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
