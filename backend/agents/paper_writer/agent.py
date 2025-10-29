"""Academic writing agent for Agora."""

import yaml
from pathlib import Path
from typing import AsyncGenerator
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.openai_client import llm_call, llm_call_with_context

class Agent:
    """Agent that writes academic-style content."""

    def __init__(self):
        self.name = "paper_writer"

        # Load config
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)

        self.description = config["description"]
        self.model = config["model"]
        self.temperature = config["temperature"]
        self.max_tokens = config.get("max_tokens", 1000)

        # Load system prompt
        prompt_path = Path(__file__).parent / "prompt.txt"
        with open(prompt_path) as f:
            self.system_prompt = f.read()

    async def run(
        self,
        query: str,
        context: list[dict],
        stream: bool = False
    ) -> str | AsyncGenerator[str, None]:
        """
        Execute the agent's task.

        Args:
            query: User's query
            context: Previous conversation messages
            stream: Whether to stream the response

        Returns:
            Agent's response as string or async generator
        """
        # Prepend system prompt to context
        messages = [{"role": "system", "content": self.system_prompt}] + context

        # Call LLM with context
        response = await llm_call_with_context(
            query=query,
            context=messages,
            model=self.model,
            temperature=self.temperature,
            stream=stream
        )

        return response
