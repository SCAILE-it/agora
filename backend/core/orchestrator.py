"""Main orchestrator for routing and executing agent requests."""

import importlib
from typing import AsyncGenerator, Optional
from .memory import MemoryManager
from .router import AgentRouter
from utils.logger import logger

class Orchestrator:
    """Coordinates agent selection, memory management, and execution."""

    def __init__(self):
        self.router = AgentRouter()
        self.memory_managers = {}  # Cache memory managers per agent

    def _get_memory_manager(self, agent_name: str) -> MemoryManager:
        """Get or create a memory manager for an agent."""
        if agent_name not in self.memory_managers:
            self.memory_managers[agent_name] = MemoryManager(agent_name)
        return self.memory_managers[agent_name]

    def _load_agent(self, agent_name: str):
        """
        Dynamically load an agent module.

        Args:
            agent_name: Name of the agent folder

        Returns:
            Agent instance
        """
        try:
            module = importlib.import_module(f"agents.{agent_name}.agent")
            agent_class = getattr(module, "Agent")
            agent_instance = agent_class()
            logger.info(f"Loaded agent: {agent_name}")
            return agent_instance
        except Exception as e:
            logger.error(f"Failed to load agent {agent_name}: {e}")
            raise ValueError(f"Agent '{agent_name}' not found or failed to load")

    async def handle_query(
        self,
        query: str,
        session_id: str,
        agent_name: Optional[str] = None,
        stream: bool = False
    ) -> str | AsyncGenerator[str, None]:
        """
        Process a user query through the appropriate agent.

        Args:
            query: User's input query
            session_id: Unique session identifier
            agent_name: Explicitly specified agent (optional)
            stream: Whether to stream the response

        Returns:
            Agent's response as string or async generator
        """
        # Route to appropriate agent
        selected_agent = self.router.route(query, agent_name)
        logger.info(f"Query routed to agent: {selected_agent}")

        # Load agent
        agent = self._load_agent(selected_agent)

        # Get memory manager for this agent
        memory = self._get_memory_manager(selected_agent)

        # Load conversation context
        context = memory.load_context(session_id, limit=5)

        # Save user query
        memory.save_message(session_id, "user", query)

        # Run agent
        try:
            response = await agent.run(query, context, stream=stream)

            if stream:
                # For streaming, we need to collect and save the response
                async def stream_and_save():
                    collected = []
                    async for chunk in response:
                        collected.append(chunk)
                        yield chunk
                    # Save complete response after streaming
                    full_response = "".join(collected)
                    memory.save_message(session_id, "assistant", full_response)

                return stream_and_save()
            else:
                # Save assistant response
                memory.save_message(session_id, "assistant", response)
                return response

        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            error_msg = f"I encountered an error: {str(e)}"
            memory.save_message(session_id, "assistant", error_msg)
            return error_msg

    def list_available_agents(self) -> list[dict]:
        """Return list of available agents with metadata."""
        agents = []
        for agent_name in self.router.list_agents():
            try:
                agent = self._load_agent(agent_name)
                agents.append({
                    "name": agent_name,
                    "description": getattr(agent, "description", "No description available"),
                    "model": getattr(agent, "model", "unknown")
                })
            except Exception as e:
                logger.warning(f"Could not load metadata for agent {agent_name}: {e}")

        return agents
