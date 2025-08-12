"""API client utilities for making authenticated requests."""

import logging
import os
from typing import cast

import httpx
from fastmcp import Context
from starlette.requests import Request as StarletteRequest

logger = logging.getLogger(__name__)


def get_token_from_context(context: Context) -> str | None:
    """Extract authentication token from MCP context."""
    request = cast(StarletteRequest, context.request_context.request)
    return request.query_params.get("token")


async def call_api_with_token(
    context: Context,
    endpoint: str,
    method: str = "GET",
    json_data: dict[str, object] | None = None,
    base_url: str | None = None,
    timeout: float = 60.0,
) -> dict[str, object]:
    """
    Make authenticated API request using Bearer token from MCP context.

    Args:
        context: MCP context containing request information
        endpoint: API endpoint path (e.g., "/auth/me")
        method: HTTP method (GET, POST, etc.)
        json_data: Optional JSON payload for POST/PUT requests
        base_url: Base URL of the API server (defaults to LANGTOOLS_API_URL env var or http://localhost:8000)
        timeout: Request timeout in seconds (default: 60.0)

    Returns:
        JSON response from the API

    Raises:
        ValueError: If no token is found in context
        httpx.HTTPError: If API request fails
    """
    token = get_token_from_context(context)
    if not token:
        raise ValueError("No authentication token found in MCP context")

    # Use provided base_url or fall back to environment variable or localhost default
    if base_url is None:
        base_url = os.getenv("LANGTOOLS_API_URL", "http://localhost:8000")

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    async with httpx.AsyncClient(timeout=timeout) as client:
        if method.upper() == "GET":
            response = await client.get(url, headers=headers)
        elif method.upper() == "POST":
            response = await client.post(url, headers=headers, json=json_data)
        elif method.upper() == "PUT":
            response = await client.put(url, headers=headers, json=json_data)
        elif method.upper() == "DELETE":
            response = await client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"API request failed: {method} {url}")
            logger.error(f"Status: {e.response.status_code}")
            logger.error(f"Response body: {e.response.text}")
            raise Exception(
                f"API request failed: {e.response.status_code} {e.response.text}"
            ) from e
        except httpx.ConnectError as e:
            logger.error(f"Failed to connect to API server: {url}")
            logger.error(f"Connection error: {e}")
            raise Exception(
                f"Failed to connect to API server at {base_url}. Check if the API server is running and accessible."
            ) from e
        except httpx.TimeoutException as e:
            logger.error(f"API request timed out: {method} {url}")
            raise Exception(f"API request timed out after {timeout}s") from e

        # httpx response.json() returns Any, cast to expected type
        return cast(dict[str, object], response.json())
