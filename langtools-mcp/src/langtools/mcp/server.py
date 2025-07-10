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

# Initialize FastMCP server with comprehensive metadata
mcp: FastMCP[Any] = FastMCP(
    name="LangTools",
    version="0.1.0",
    instructions=(
        "LangTools: AI-Powered Language Learning Companion. "
        "This server provides comprehensive multilingual dictionary tools designed to enhance language learning through detailed, educational responses. "
        "When working with users, be patient, encouraging, and educational. Always show complete dictionary entries with all details - "
        "pronunciations, multiple meanings, cultural contexts, and synonyms - as each component serves a specific learning purpose. "
        "Encourage users to practice pronunciation, use words in context, and build connections to previously learned vocabulary. "
        "Your role is not just translation, but comprehensive language education and cultural understanding."
    ),
)

# Define help prompt text
HELP_PROMPT = """You are now equipped with langtools - powerful AI-powered language learning tools through MCP integration.

## Available Tools

### Dictionary Generation
- **Tool**: `generate_dictionary_entry_tool`
- **Purpose**: Generate comprehensive multilingual dictionary entries
- **Usage**: Provide a term, your language preferences, and target language
- **Features**:
  - Multiple meanings and contexts
  - Accurate translations
  - Pronunciation guides (IPA format)
  - Synonyms and related terms
  - Definitions in both source and target languages

## How to Use Langtools

### Basic Dictionary Lookup
When a user asks about a word or phrase:
1. Use the dictionary tool to get comprehensive information
2. Present the results in a clear, educational format
3. Encourage pronunciation practice
4. Suggest related vocabulary

### Language Learning Support
- **Vocabulary Building**: Generate entries for new words encountered
- **Translation Help**: Provide context-aware translations
- **Pronunciation Aid**: Always include pronunciation guides
- **Cultural Context**: Use the tool's multiple meanings to explain cultural nuances

### Example Usage Patterns
- "What does 'hello' mean in Spanish?" → Use dictionary tool
- "How do you pronounce 'bonjour'?" → Use dictionary tool for pronunciation
- "I'm learning German, what are some ways to say 'good'?" → Use dictionary tool for synonyms

## Best Practices
1. **Always provide pronunciation**: Help users learn correct pronunciation
2. **Context matters**: Explain different meanings and when to use each
3. **Encourage practice**: Suggest the user try using the words in sentences
4. **Build vocabulary**: Connect new words to previously learned ones
5. **Be patient and encouraging**: Language learning takes time and practice

Remember: You're not just translating - you're teaching and supporting language learning!"""


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
    Generate comprehensive multilingual dictionary entry for enhanced language learning.

    This tool creates detailed dictionary entries with multiple meanings, accurate translations,
    IPA pronunciations, and contextual synonyms. The output is designed to be educational and
    comprehensive - ALWAYS show the complete results to users, as each component serves a specific
    learning purpose.

    BEHAVIORAL GUIDANCE:
    - Display ALL returned meanings, translations, and pronunciations to the user
    - Encourage users to practice pronunciation using the IPA guides provided
    - Explain when to use different meanings based on context
    - Suggest creating example sentences with the new vocabulary
    - Connect new words to previously learned vocabulary when possible
    - Be patient and encouraging - language learning is a gradual process

    EDUCATIONAL VALUE:
    - Multiple meanings: Help users understand nuanced usage
    - Pronunciations: Enable proper speaking and listening skills
    - Synonyms: Expand vocabulary and provide alternatives
    - Definitions: Support reading comprehension and writing skills
    - Cultural context: Enable appropriate usage in different situations

    Args:
        translating_term: The word or phrase to define and translate
        user_learning_languages: User's language preferences in format 'en:1,ru:2'
        translation_language: Target language for translations in BCP 47 format
        model: LLM model to use for generation

    Returns:
        Dictionary containing comprehensive multilingual information with meanings,
        translations, pronunciations (IPA), definitions in both languages, and synonyms.
        Present this information in full to maximize educational benefit.

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


@mcp.prompt()
async def help_prompt() -> str:
    """
    Langtools Usage Guide - How to use language learning tools effectively.

    This prompt provides comprehensive guidance on using the langtools MCP server
    for language learning, including tool usage patterns, best practices, and
    educational approaches.

    Returns:
        Full prompt text with langtools usage instructions
    """
    return HELP_PROMPT


def create_server() -> FastMCP[Any]:
    """Create and configure the MCP server."""
    return mcp


if __name__ == "__main__":
    mcp.run()
