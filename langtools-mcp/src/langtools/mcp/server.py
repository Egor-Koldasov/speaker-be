"""MCP server implementation for language learning tools."""

import logging

from typing import Any

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from langtools.ai.debug import configure_debug_logging
from langtools.ai.functions import generate_dictionary_entry
from langtools.ai.models import AiDictionaryEntry, DictionaryEntryParams, ModelType


class DictionaryGenerationError(Exception):
    """Raised when dictionary generation fails."""


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure debug logging
configure_debug_logging()

# Initialize FastMCP server
mcp: FastMCP[Any] = FastMCP("langtools-mcp")


class DictionaryEntryRequest(BaseModel):
    """Request model for dictionary entry generation."""

    translating_term: str = Field(description="The word or phrase to define and translate")
    user_learning_languages: str = Field(
        description="User's language preferences in format 'en:1,ru:2'"
    )
    translation_language: str = Field(
        description="Target language for translations in BCP 47 format"
    )
    model: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="LLM model to use for generation",
    )


@mcp.tool()
async def generate_dictionary_entry_tool(
    translating_term: str,
    user_learning_languages: str,
    translation_language: str,
    model: str = "claude-3-5-sonnet-20241022",
) -> dict[str, Any]:
    """
    Generate comprehensive dictionary entry for a term using AI.

    This tool creates multilingual dictionary entries with definitions,
    translations, pronunciations, and synonyms for language learning.

    Args:
        translating_term: The word or phrase to define and translate
        user_learning_languages: User's language preferences in format 'en:1,ru:2'
        translation_language: Target language for translations in BCP 47 format
        model: LLM model to use for generation

    Returns:
        Dictionary containing comprehensive multilingual information

    Raises:
        Exception: If generation fails due to validation or API errors
    """
    try:
        logger.info(f"Generating dictionary entry for: {translating_term}")

        # Convert parameters to DictionaryEntryParams
        params = DictionaryEntryParams(
            translating_term=translating_term,
            user_learning_languages=user_learning_languages,
            translation_language=translation_language,
        )

        # Convert model string to ModelType enum
        try:
            model_type = ModelType(model)
        except ValueError:
            # Default to Claude Sonnet if invalid model provided
            model_type = ModelType.CLAUDE_SONNET
            logger.warning(f"Invalid model {model}, using default: {model_type.value}")

        # Call the AI function
        result: AiDictionaryEntry = await generate_dictionary_entry(params, model_type)

        # Convert Pydantic model to dict for MCP response
        response = result.model_dump()

        logger.info(f"Successfully generated dictionary entry with {len(result.meanings)} meanings")
        logger.debug(f"Response: {response}")
        return response

    except Exception as e:
        logger.exception("Failed to generate dictionary entry")
        error_msg = f"Dictionary entry generation failed: {e!s}"
        raise DictionaryGenerationError(error_msg) from e


def create_server() -> FastMCP[Any]:
    """Create and configure the MCP server."""
    return mcp


if __name__ == "__main__":
    mcp.run()
