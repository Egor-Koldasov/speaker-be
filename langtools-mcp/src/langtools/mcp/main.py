"""CLI entry point for langtools-mcp server."""

import argparse
import logging
import sys

from .server import mcp


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Language learning tools MCP server")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--version", action="version", version="langtools-mcp 0.1.0")
    return parser.parse_args()


def main() -> None:
    """Main CLI entry point."""
    args = parse_args()

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    try:
        logger.info("Starting langtools-mcp server...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception:
        logger.exception("Server failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
