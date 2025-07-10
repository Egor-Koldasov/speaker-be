"""
Debug configuration utilities for langtools packages.
"""

import logging
import os

from langchain.globals import set_debug


logger = logging.getLogger(__name__)


def configure_debug_logging() -> None:
    """Configure debug logging for langtools packages based on LANGTOOLS_DEBUG environment variable."""
    if os.getenv("LANGTOOLS_DEBUG", "false").lower() == "true":
        # Enable LangChain debug mode
        set_debug(True)

        # Configure detailed logging for LangChain components
        logging.getLogger("langchain").setLevel(logging.DEBUG)
        logging.getLogger("langchain.chains").setLevel(logging.DEBUG)
        logging.getLogger("langchain.llms").setLevel(logging.DEBUG)
        logging.getLogger("langchain.chat_models").setLevel(logging.DEBUG)
        logging.getLogger("langchain.callbacks").setLevel(logging.DEBUG)
        logging.getLogger("langchain.prompts").setLevel(logging.DEBUG)
        logging.getLogger("langchain.schema").setLevel(logging.DEBUG)
        logging.getLogger("langchain_core").setLevel(logging.DEBUG)
        logging.getLogger("langchain_openai").setLevel(logging.DEBUG)
        logging.getLogger("langchain_anthropic").setLevel(logging.DEBUG)

        # Configure detailed logging for AI API clients
        logging.getLogger("anthropic").setLevel(logging.DEBUG)
        logging.getLogger("openai").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logging.getLogger("httpcore").setLevel(logging.DEBUG)

        logger.info("Debug logging enabled for LangChain and API clients")
