"""Agent routing logic based on intent detection."""

from typing import Optional
from utils.logger import logger

class AgentRouter:
    """Routes user queries to appropriate agents based on keywords."""

    def __init__(self):
        # Define keyword mappings for each agent
        self.agent_keywords = {
            "paper_writer": ["write", "academic", "paper", "research", "essay", "paragraph"],
            "shopper": ["buy", "shop", "product", "price", "amazon", "search", "find"],
        }
        self.default_agent = "paper_writer"

    def route(self, query: str, explicit_agent: Optional[str] = None) -> str:
        """
        Determine which agent should handle the query.

        Args:
            query: User query text
            explicit_agent: Explicitly specified agent name (from UI selector)

        Returns:
            Agent name to use
        """
        # If user explicitly selected an agent, use that
        if explicit_agent and self._is_valid_agent(explicit_agent):
            logger.info(f"Using explicitly selected agent: {explicit_agent}")
            return explicit_agent

        # Check for slash commands (e.g., "/paper write something")
        if query.startswith("/"):
            parts = query.split(maxsplit=1)
            if len(parts) > 0:
                potential_agent = parts[0][1:]  # Remove the "/"
                if self._is_valid_agent(potential_agent):
                    logger.info(f"Detected slash command for agent: {potential_agent}")
                    return potential_agent

        # Keyword-based routing
        query_lower = query.lower()
        agent_scores = {}

        for agent, keywords in self.agent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                agent_scores[agent] = score

        if agent_scores:
            # Return agent with highest score
            best_agent = max(agent_scores, key=agent_scores.get)
            logger.info(f"Routed to {best_agent} based on keywords (score: {agent_scores[best_agent]})")
            return best_agent

        # Default fallback
        logger.info(f"No specific agent detected, using default: {self.default_agent}")
        return self.default_agent

    def _is_valid_agent(self, agent_name: str) -> bool:
        """Check if an agent name exists in our registry."""
        return agent_name in self.agent_keywords

    def list_agents(self) -> list[str]:
        """Return list of available agent names."""
        return list(self.agent_keywords.keys())
