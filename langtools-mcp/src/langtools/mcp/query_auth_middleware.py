from typing import cast
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from starlette.requests import Request as StarletteRequest


class QueryAuthMiddleware(Middleware):
    async def on_message(
        self, context: MiddlewareContext[None], call_next: CallNext[None, None]
    ) -> None:
        assert context.fastmcp_context is not None
        request = cast(StarletteRequest, context.fastmcp_context.request_context.request)
        token = request.query_params.get("token")
        print(token)

        return await call_next(context)
