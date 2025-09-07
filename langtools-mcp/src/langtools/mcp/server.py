"""MCP server implementation for language learning tools."""

import logging
from datetime import datetime
from typing import Optional, cast

from fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

from langtools.ai.debug import configure_debug_logging
from langtools.mcp.convex import call_convex
from langtools.mcp.query_auth_middleware import QueryAuthMiddleware


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
    stateless_http=True,
)

mcp.add_middleware(QueryAuthMiddleware())

# Define help prompt text
HELP_PROMPT = """You are now equipped with langtools - powerful AI-powered language \
learning tools through MCP integration.

## Available Tools

### Dictionary Generation
- **Tool**: `generate_dictionary_entry`
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
    model: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="LLM model to use for generation",
    )


async def generate_dictionary_entry(
    context: Context,
    translating_term: str,
    force_language: Optional[str] = None,
    regenerate_full: bool = False,
) -> dict[str, object]:
    """
    Generate comprehensive dictionary entry using the langtools API.
    """
    try:
        logger.info(f"Generating dictionary entry for: {translating_term}")

        args: dict[str, object] = {
            "headword": translating_term,
            "forceLanguage": force_language,
            "regenerateFull": regenerate_full,
        }
        if not args["forceLanguage"]:
            del args["forceLanguage"]

        response = cast(
            dict[str, object],
            await call_convex(
                context,
                "aiChat:generateDictionaryEntryComplete",
                operation="action",
                args=args,
            ),
        )

        logger.info(f"Successfully generated dictionary entry for: {translating_term}")
        return response

    except Exception as e:
        logger.exception("Failed to generate dictionary entry")
        error_msg = f"Dictionary entry generation failed: {e!s}"
        raise DictionaryGenerationError(error_msg) from e


# Register the tool as enabled
mcp.tool()(generate_dictionary_entry)


@mcp.tool()
async def get_fsrs_records(
    context: Context,
    page: int = 1,
    page_size: int = 20,
) -> list[dict[str, object]]:
    """
    Get paginated list of FSRS spaced repetition records for the current user.
    """
    try:
        logger.info(f"Getting FSRS records for user, page {page}, size {page_size}")

        response = cast(
            list[dict[str, object]],
            await call_convex(context, "fsrsProgress:getFsrsProgressList"),
        )

        logger.info(f"Successfully retrieved FSRS records: {len(response)} total")
        logger.info(f"FSRS records: {response}")
        return response

    except Exception as e:
        logger.exception("Failed to get FSRS records")
        raise Exception(f"Failed to retrieve FSRS records: {e}") from e


@mcp.tool()
async def create_fsrs_record(
    context: Context,
    sense_id: str,
) -> dict[str, object]:
    """
    Create a new FSRS spaced repetition record for vocabulary training.
    """
    try:
        request_data: dict[str, object] = {
            "senseId": sense_id,
        }

        response = cast(
            dict[str, object],
            await call_convex(
                context=context,
                path="fsrsProgress:createFsrsProgress",
                operation="mutation",
                args=request_data,
            ),
        )

        logger.info(f"Successfully created FSRS record: {response.get('fsrs_id')}")
        return response

    except Exception as e:
        logger.exception("Failed to create FSRS record")
        raise Exception(f"Failed to create FSRS record: {e}") from e


@mcp.tool()
async def process_fsrs_review(
    context: Context,
    fsrs_progress_id: str,
    rating: int,
) -> dict[str, object]:
    """
    Process a spaced repetition review session and update training data.
    """
    try:
        logger.info(f"Processing review for FSRS record {fsrs_progress_id} with rating {rating}")

        # Validate rating
        if rating not in [1, 2, 3, 4]:
            raise ValueError(
                f"Invalid rating {rating}. Must be 1 (Again), 2 (Hard), 3 (Good), or 4 (Easy)"
            )

        # Prepare request data
        request_data: dict[str, object] = {
            "rating": rating,
            "fsrsProgressId": fsrs_progress_id,
        }

        # Call the API
        response = cast(
            dict[str, object],
            await call_convex(
                context=context,
                path="fsrsProgress:processReview",
                operation="action",
                args=request_data,
            ),
        )

        logger.info(f"Successfully processed review for FSRS record: {fsrs_progress_id}")
        return response

    except Exception as e:
        logger.exception("Failed to process FSRS review")
        raise Exception(f"Failed to process review: {e}") from e


@mcp.tool()
async def me(context: Context) -> dict[str, object]:
    """
    Get current user information using authentication token from MCP context.
    """
    try:
        logger.info("Getting current user info via /auth/me endpoint")

        # Call the API with the token from context
        response = cast(dict[str, object], await call_convex(context=context, path="users:getUser"))

        return response

    except ValueError as e:
        logger.error(f"Authentication error: {e}")
        raise Exception(f"Authentication required: {e}") from e
    except Exception as e:
        logger.exception("Failed to get current user info")
        raise Exception(f"Failed to retrieve user information: {e}") from e


class DatetimeNowResponse(BaseModel):
    """Response model for datetime_now tool."""

    datetime_iso: str = Field(description="Current datetime in ISO 8601 format with timezone")


async def datetime_now() -> DatetimeNowResponse:
    """
    Get the current datetime in ISO format with timezone information.

    Returns:
        Current datetime as an ISO 8601 formatted string with timezone
        (YYYY-MM-DDTHH:MM:SS.ssssss+HH:MM)
    """
    return DatetimeNowResponse(datetime_iso=datetime.now().astimezone().isoformat())


# Register datetime_now tool
mcp.tool()(datetime_now)


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
