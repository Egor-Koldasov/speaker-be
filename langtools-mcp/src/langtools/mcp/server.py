"""MCP server implementation for language learning tools."""

import logging


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
mcp = FastMCP(
    name="LangTools",
    version="0.1.0",
    instructions=(
        "LangTools: AI-Powered Language Learning Companion. "
        "This server provides comprehensive multilingual dictionary tools designed to "
        "enhance language learning through detailed, educational responses. "
        "When working with users, be patient, encouraging, and educational. Always show "
        "complete dictionary entries with all details - pronunciations, multiple meanings, "
        "cultural contexts, and synonyms - as each component serves a specific learning "
        "purpose. Encourage users to practice pronunciation, use words in context, and "
        "build connections to previously learned vocabulary. Your role is not just "
        "translation, but comprehensive language education and cultural understanding."
    ),
)

# Define help prompt text
HELP_PROMPT = """You are now equipped with langtools - powerful AI-powered language \
learning tools through MCP integration.

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


@mcp.tool(enabled=False)
async def generate_dictionary_entry_tool(
    translating_term: str,
    user_learning_languages: str,
    translation_language: str,
    model: str = "claude-4-0-sonnet",
) -> dict[str, object]:
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
        response: dict[str, object] = result.model_dump()

        logger.info(f"Successfully generated dictionary entry with {len(result.meanings)} meanings")
        logger.debug(f"Response: {response}")
        return response

    except Exception as e:
        logger.exception("Failed to generate dictionary entry")
        error_msg = f"Dictionary entry generation failed: {e!s}"
        raise DictionaryGenerationError(error_msg) from e


@mcp.tool()
async def check_dictionary_entry(
    generation_parameters: DictionaryEntryParams,
    dictionary_entry: AiDictionaryEntry,
) -> str:
    """
    Validate and confirm a client-generated dictionary entry for language learning.

    🎯 **IMPORTANT: Call this tool EVERY TIME a user asks for word definitions, \
translations, or language help!**

    ## How This Works

    The purpose of this function is to generate the most detailed and comprehensive
    dictionary entry.

    - The definition entry should strive for the best dictionary level of quality and
    accuracy.
    - The definition should include as many meanings as possible, including rare usages
    and folklore.
    - You, the AI agent, is responsible for generating the dictionary entry yourself.
    This tool serves as an instruction of the proper format and requirements for the \
dictionary entry.

    ## User Presentation

    After calling this tool, consider presenting the full dictionary information from the JSON
    in a human-readable format that includes pronunciations, meanings, translations, and synonyms
    to provide comprehensive language learning value.

    Args:
        generation_parameters: Input parameters for the dictionary lookup
        dictionary_entry: Complete dictionary entry with all required fields

    Returns:
        Confirmation message indicating successful validation and processing
    """
    try:
        # Validate that the entry matches the generation parameters
        term = generation_parameters.translating_term.lower().strip()
        entry_terms = [
            meaning.neutral_form.lower().strip() for meaning in dictionary_entry.meanings
        ]

        if not any(term in entry_term or entry_term in term for entry_term in entry_terms):
            return (
                f"⚠️ Warning: The dictionary entry doesn't seem to match the requested "
                f"term '{term}'. Please verify the entry corresponds to the correct word."
            )

        # Validate completeness
        total_meanings = len(dictionary_entry.meanings)
        if total_meanings == 0:
            return "❌ Error: Dictionary entry must contain at least one meaning."

        # Confirm successful validation
        logger.info(
            f"Successfully validated dictionary entry for '{term}' with {total_meanings} meaning(s)"
        )

        return (
            f"✅ Dictionary entry successfully validated! Found {total_meanings} meaning(s) "
            f"for '{term}'. The entry is properly formatted and ready for educational "
            f"presentation to the user."
        )

    except (ValueError, TypeError, AttributeError) as e:
        logger.exception("Error validating dictionary entry")
        return (
            f"❌ Validation error: {e!s}. Please ensure the dictionary entry follows the "
            f"required schema format."
        )


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


def create_server():
    """Create and configure the MCP server."""
    return mcp


if __name__ == "__main__":
    mcp.run()
