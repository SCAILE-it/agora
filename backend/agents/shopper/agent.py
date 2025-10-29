"""Shopping agent for product recommendations."""

import yaml
from pathlib import Path
from typing import AsyncGenerator
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.openai_client import llm_call_with_context
from .tools import search_amazon

class Agent:
    """Agent that helps find and recommend products."""

    def __init__(self):
        self.name = "shopper"

        # Load config
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)

        self.description = config["description"]
        self.model = config["model"]
        self.temperature = config["temperature"]
        self.max_tokens = config.get("max_tokens", 800)

    async def run(
        self,
        query: str,
        context: list[dict],
        stream: bool = False
    ) -> str | AsyncGenerator[str, None]:
        """
        Execute shopping search and recommendations.

        Args:
            query: User's product query
            context: Previous conversation messages
            stream: Whether to stream the response

        Returns:
            Product recommendations as string or async generator
        """
        # Use tool to get product data
        product_data = search_amazon(query)

        # Create enhanced prompt with product data
        system_prompt = f"""You are a helpful shopping assistant.

Here are some product results I found:

{product_data}

Based on these results and the user's query, provide helpful shopping advice,
compare options, and make recommendations. Be friendly and concise."""

        messages = [{"role": "system", "content": system_prompt}] + context

        # Get LLM to format and explain the recommendations
        response = await llm_call_with_context(
            query=query,
            context=messages,
            model=self.model,
            temperature=self.temperature,
            stream=stream
        )

        return response
