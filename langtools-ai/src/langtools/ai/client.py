"""
LLM client management for AI functions.
"""

from typing import Any
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.callbacks.manager import get_openai_callback
from .models import ModelType


class LLMClient:
    """Client for managing LLM interactions with different providers."""
    
    def __init__(self, model_type: ModelType) -> None:
        """Initialize client with specified model type."""
        self.model_type = model_type
        self.model = self._create_model(model_type)
    
    def _create_model(self, model_type: ModelType) -> Any:
        """Create appropriate LangChain model based on type."""
        if model_type in [ModelType.GPT4, ModelType.GPT3_5]:
            return ChatOpenAI(
                model=model_type.value,
                temperature=0.3,
                max_tokens=8000,
                timeout=180
            )
        elif model_type in [ModelType.CLAUDE_SONNET, ModelType.CLAUDE_SONNET_4]:
            return ChatAnthropic(
                model=model_type.value,
                temperature=0.3,
                max_tokens=8000,
                timeout=180
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    async def generate_with_parser(self, chain: Any) -> Any:
        """Execute LangChain chain with cost logging."""
        print("🚀 DEBUG: Executing LLM chain...")
        
        if self.model_type in [ModelType.GPT4, ModelType.GPT3_5]:
            with get_openai_callback() as cb:
                result = await chain.ainvoke({})
                # Log cost information for monitoring
                print(f"💰 LLM API cost: ${cb.total_cost:.4f}")
                return result
        else:
            result = await chain.ainvoke({})
            print("✅ DEBUG: LLM chain execution completed successfully")
            return result