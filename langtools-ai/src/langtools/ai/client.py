"""
LLM client management for AI functions.
"""

from __future__ import annotations

import logging
from typing import List

from langchain_anthropic import ChatAnthropic
from langchain_community.callbacks.manager import get_openai_callback
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

from langtools.ai.debug import configure_debug_logging

from .models import AiDictionaryEntry, AiMeaningTranslation, MeaningTranslationList, ModelType

logger = logging.getLogger(__name__)

configure_debug_logging()


class LLMClient:
    """Client for managing LLM interactions with different providers."""

    def __init__(self, model_type: ModelType) -> None:
        """Initialize client with specified model type."""
        self.model_type = model_type
        self.model = self._create_model(model_type)

    def _create_model(self, model_type: ModelType) -> BaseChatModel:
        """Create appropriate LangChain model based on type."""
        if model_type in [
            ModelType.GPT4,
            ModelType.GPT3_5,
            ModelType.GTP4_1_MINI,
            ModelType.GTP5_MINI,
            ModelType.GTP4_O_MINI,
        ]:
            # Use fewer tokens for GPT models to avoid context length issues
            return ChatOpenAI(
                model=model_type.value,
                temperature=1 if model_type == ModelType.GTP5_MINI else 0.3,
                max_tokens=32768  # type: ignore[call-arg]
                if model_type == ModelType.GTP4_1_MINI
                else 16384
                if model_type == ModelType.GTP4_O_MINI
                else 64000,
                timeout=180,  # type: ignore[call-arg]
            )
        if model_type in [ModelType.CLAUDE_SONNET_3_5, ModelType.CLAUDE_SONNET_4]:
            # Enable thinking only for Sonnet 4.0
            thinking_config = None
            if model_type == ModelType.CLAUDE_SONNET_4:
                thinking_config = {
                    "type": "enabled",
                    "budget_tokens": 32000,
                }

            return ChatAnthropic(
                model=model_type.value,  # type: ignore[call-arg]
                max_tokens=64000,  # type: ignore[call-arg]
                timeout=180,  # type: ignore[call-arg]
                thinking=thinking_config,
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

    async def generate_with_parser_base(
        self, chain: Runnable[dict[str, str], AiDictionaryEntry]
    ) -> AiDictionaryEntry:
        """Execute base dictionary chain with cost logging."""
        logger.info("🚀 Executing base dictionary LLM chain...")

        if self.model_type in [ModelType.GPT4, ModelType.GPT3_5]:
            with get_openai_callback() as cb:
                result = await chain.ainvoke({})
                # Log cost information for monitoring
                logger.info(f"💰 Base dictionary API cost: ${cb.total_cost:.4f}")
                return result
        else:
            result = await chain.ainvoke({})
            logger.info("✅ Base dictionary chain execution completed successfully")
            return result

    async def generate_with_parser_translations(
        self, chain: Runnable[dict[str, str], MeaningTranslationList]
    ) -> List[AiMeaningTranslation]:
        """Execute translation chain with cost logging."""
        logger.info("🚀 Executing translation LLM chain...")

        if self.model_type in [ModelType.GPT4, ModelType.GPT3_5]:
            with get_openai_callback() as cb:
                result = await chain.ainvoke({})
                # Log cost information for monitoring
                logger.info(f"💰 Translation API cost: ${cb.total_cost:.4f}")
                return result.translations
        else:
            result = await chain.ainvoke({})
            logger.info("✅ Translation chain execution completed successfully")
            return result.translations
