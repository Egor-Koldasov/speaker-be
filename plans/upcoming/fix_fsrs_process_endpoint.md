# Fix the error of fsrs processing endpoint

Given a new fsrs record
Run `/process_review` with these parameters 2 times

```json
{
  "rating": 3,
  "review_time": "2025-08-11T05:29:36.830Z"
}
```
The API encounters an error
```
langtools-api       | ERROR:    Exception in ASGI application
langtools-api       | Traceback (most recent call last):
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/uvicorn/protocols/http/httptools_impl.py", line 409, in run_asgi
langtools-api       |     result = await app(  # type: ignore[func-returns-value]
langtools-api       |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
langtools-api       |     return await self.app(scope, receive, send)
langtools-api       |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
langtools-api       |     await super().__call__(scope, receive, send)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/applications.py", line 113, in __call__
langtools-api       |     await self.middleware_stack(scope, receive, send)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
langtools-api       |     raise exc
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
langtools-api       |     await self.app(scope, receive, _send)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 93, in __call__
langtools-api       |     await self.simple_response(scope, receive, send, request_headers=headers)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 144, in simple_response
langtools-api       |     await self.app(scope, receive, send)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
langtools-api       |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
langtools-api       |     raise exc
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
langtools-api       |     await app(scope, receive, sender)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/routing.py", line 716, in __call__
langtools-api       |     await self.middleware_stack(scope, receive, send)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/routing.py", line 736, in app
langtools-api       |     await route.handle(scope, receive, send)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/routing.py", line 290, in handle
langtools-api       |     await self.app(scope, receive, send)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/routing.py", line 78, in app
langtools-api       |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
langtools-api       |     raise exc
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
langtools-api       |     await app(scope, receive, sender)
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/routing.py", line 75, in app
langtools-api       |     response = await f(request)
langtools-api       |                ^^^^^^^^^^^^^^^^
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/fastapi/routing.py", line 302, in app
langtools-api       |     raw_response = await run_endpoint_function(
langtools-api       |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/fastapi/routing.py", line 215, in run_endpoint_function
langtools-api       |     return await run_in_threadpool(dependant.call, **values)
langtools-api       |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/starlette/concurrency.py", line 38, in run_in_threadpool
langtools-api       |     return await anyio.to_thread.run_sync(func)
langtools-api       |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/anyio/to_thread.py", line 56, in run_sync
langtools-api       |     return await get_async_backend().run_sync_in_worker_thread(
langtools-api       |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 2470, in run_sync_in_worker_thread
langtools-api       |     return await future
langtools-api       |            ^^^^^^^^^^^^
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 967, in run
langtools-api       |     result = context.run(func, *args)
langtools-api       |              ^^^^^^^^^^^^^^^^^^^^^^^^
langtools-api       |   File "/workspace-root/langtools-main/src/langtools/main/api/routers/fsrs.py", line 183, in process_review_endpoint
langtools-api       |     updated = process_review(current, request.rating, review_time)
langtools-api       |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
langtools-api       |   File "/workspace-root/langtools-main/src/langtools/main/fsrs/functions.py", line 68, in process_review
langtools-api       |     updated_py_card, _ = _DEFAULT_SCHEDULER.review_card(py_card, py_rating, review_time)
langtools-api       |                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
langtools-api       |   File "/tmp/venv/lib/python3.11/site-packages/fsrs/scheduler.py", line 246, in review_card
langtools-api       |     (review_datetime - card.last_review).days if card.last_review else None
langtools-api       |      ~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~
langtools-api       | TypeError: can't subtract offset-naive and offset-aware datetimes
langtools-api       | INFO:     192.168.65.1:38042 - "POST /fsrs/01989796-fe6f-7f10-9893-ca5ff11e5695/process_review HTTP/1.1" 500 Internal Server
```

