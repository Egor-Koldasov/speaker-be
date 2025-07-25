"""
LLM client management for AI functions.
"""

from __future__ import annotations

import logging

from langchain_anthropic import ChatAnthropic
from langchain_community.callbacks.manager import get_openai_callback
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

from .models import AiDictionaryEntry, ModelType

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for managing LLM interactions with different providers."""

    def __init__(self, model_type: ModelType) -> None:
        """Initialize client with specified model type."""
        self.model_type = model_type
        self.model = self._create_model(model_type)

    def _create_model(self, model_type: ModelType) -> BaseChatModel:
        """Create appropriate LangChain model based on type."""
        if model_type in [ModelType.GPT4, ModelType.GPT3_5]:
            # Use fewer tokens for GPT models to avoid context length issues
            max_tokens = 4000 if model_type == ModelType.GPT3_5 else 6000
            return ChatOpenAI(
                model=model_type.value,
                temperature=0.3,
                max_tokens=max_tokens,  # type: ignore[call-arg]
                timeout=180,  # type: ignore[call-arg]
            )
        if model_type in [ModelType.CLAUDE_SONNET, ModelType.CLAUDE_SONNET_4]:
            return ChatAnthropic(
                model=model_type.value,  # type: ignore[call-arg]
                temperature=0.3,
                max_tokens=8000,  # type: ignore[call-arg]
                timeout=180,  # type: ignore[call-arg]
            )

        error_msg = f"Unsupported model type: {model_type}"
        raise ValueError(error_msg)

    async def generate_with_parser(
        self, chain: Runnable[dict[str, str], AiDictionaryEntry]
    ) -> AiDictionaryEntry:
        """Execute LangChain chain with cost logging."""
        logger.info("🚀 Executing LLM chain...")

        if self.model_type in [ModelType.GPT4, ModelType.GPT3_5]:
            with get_openai_callback() as cb:
                result = await chain.ainvoke({})
                # Log cost information for monitoring
                logger.info(f"💰 LLM API cost: ${cb.total_cost:.4f}")
                return result
        else:
            result = await chain.ainvoke({})
            logger.info("✅ LLM chain execution completed successfully")
            return result
