"""API client utilities for making authenticated requests."""

import httpx
from typing import cast
from fastmcp import Context
from starlette.requests import Request as StarletteRequest


def get_token_from_context(context: Context) -> str | None:
    """Extract authentication token from MCP context."""
    request = cast(StarletteRequest, context.request_context.request)
    return request.query_params.get("token")


async def call_api_with_token(
    context: Context,
    endpoint: str,
    method: str = "GET",
    json_data: dict[str, object] | None = None,
    base_url: str = "http://localhost:8000",
) -> dict[str, object]:
    """
    Make authenticated API request using Bearer token from MCP context.

    Args:
        context: MCP context containing request information
        endpoint: API endpoint path (e.g., "/auth/me")
        method: HTTP method (GET, POST, etc.)
        json_data: Optional JSON payload for POST/PUT requests
        base_url: Base URL of the API server

    Returns:
        JSON response from the API

    Raises:
        ValueError: If no token is found in context
        httpx.HTTPError: If API request fails
    """
    token = get_token_from_context(context)
    if not token:
        raise ValueError("No authentication token found in MCP context")

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    async with httpx.AsyncClient() as client:
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

        response.raise_for_status()
        # httpx response.json() returns Any, cast to expected type
        return cast(dict[str, object], response.json())
