import logging
import os
from dataclasses import dataclass
from typing import Annotated, Any, cast

from convex import ConvexClient
from fastmcp import Context
from starlette.requests import Request as StarletteRequest

from langtools.mcp.api import call_api_with_token

convexUrl = os.getenv("CONVEX_URL", "https://deafening-husky-833.convex.cloud")

convex = ConvexClient(convexUrl)
logger = logging.getLogger(__name__)


def get_token_from_context(context: Context) -> str | None:
    """Extract authentication token from MCP context."""
    request = cast(StarletteRequest, context.request_context.request)
    return request.query_params.get("token")


def require_token_from_context(context: Context) -> str:
    """Require authentication token from MCP context."""
    token = get_token_from_context(context)
    if not token:
        raise ValueError("No authentication token found in MCP context")
    return token


ConvexQueryResult = Annotated[Any, "The result of a Convex query"]  # pyright: ignore[reportExplicitAny]


@dataclass
class ConvexQueryRequestResult:
    value: ConvexQueryResult  # pyright: ignore[reportExplicitAny]
    status: str


async def call_convex_query(  # pyright: ignore[reportAny]
    context: Context, query: str, args: dict[str, object] = {}
) -> ConvexQueryResult:  # pyright: ignore[reportExplicitAny]
    """Call a Convex query and return the result."""

    logger.info(f"convexUrl: {convexUrl}")
    result = await call_api_with_token(
        context=context,
        endpoint="/api/query",
        method="POST",
        json_data={"path": query, "args": args, "format": "json"},
        base_url=convexUrl,
    )

    if result["status"] != "success":
        raise Exception(result)
    return result["value"]
