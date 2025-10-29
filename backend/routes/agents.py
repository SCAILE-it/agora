"""API routes for listing and managing agents."""

from fastapi import APIRouter
from core.orchestrator import Orchestrator

router = APIRouter(prefix="/agents", tags=["agents"])
orchestrator = Orchestrator()

@router.get("/")
async def list_agents():
    """
    Get list of available agents.

    Returns:
        List of agent metadata
    """
    agents = orchestrator.list_available_agents()
    return {"agents": agents, "count": len(agents)}

@router.get("/{agent_name}")
async def get_agent_info(agent_name: str):
    """
    Get detailed information about a specific agent.

    Args:
        agent_name: Name of the agent

    Returns:
        Agent metadata
    """
    agents = orchestrator.list_available_agents()
    agent = next((a for a in agents if a["name"] == agent_name), None)

    if not agent:
        return {"error": f"Agent '{agent_name}' not found"}, 404

    return agent
