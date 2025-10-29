"""OpenAI API client with streaming support."""

import os
from typing import AsyncGenerator
from openai import AsyncOpenAI
from dotenv import load_dotenv
from .logger import logger

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def llm_call(
    prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    max_tokens: int = 1000,
    stream: bool = False
) -> str | AsyncGenerator[str, None]:
    """
    Call OpenAI API with the given prompt.

    Args:
        prompt: The user prompt
        model: OpenAI model name
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        stream: Whether to stream the response

    Returns:
        Complete response string or async generator of chunks
    """
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )

        if stream:
            async def stream_response():
                async for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            return stream_response()
        else:
            return response.choices[0].message.content

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise

async def llm_call_with_context(
    query: str,
    context: list[dict],
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    stream: bool = False
) -> str | AsyncGenerator[str, None]:
    """
    Call OpenAI API with conversation context.

    Args:
        query: Current user query
        context: List of previous messages [{"role": "user/assistant", "content": "..."}]
        model: OpenAI model name
        temperature: Sampling temperature
        stream: Whether to stream the response

    Returns:
        Complete response string or async generator of chunks
    """
    try:
        messages = context + [{"role": "user", "content": query}]

        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream
        )

        if stream:
            async def stream_response():
                async for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            return stream_response()
        else:
            return response.choices[0].message.content

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise
