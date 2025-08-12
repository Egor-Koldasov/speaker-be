# Fix MCP in docker on VPS

When MCP server is running directly on the VPS, it works correctly, but when running in docker, it returns an error when I connect with MCP inspector.


Here are the logs from the MCP server when running directly on the VPS. Everything works fine.
```
INFO:     172.70.208.55:0 - "POST /mcp?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrb2xkYXNvdjNAZ21haWwuY29tIiwiZXhwIjoiMTc1NzU4NDQ4MyJ9.tl6o_490NmrJqHYp8a23bhHiWVEgrASpTAxNA8ZVCII HTTP/1.1" 307 Temporary Redirect
^[[IINFO:mcp.server.streamable_http_manager:Created new transport with session ID: 4c270db1d4344d9f891feffcd3d693a8
INFO:     172.68.44.141:0 - "POST /mcp/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrb2xkYXNvdjNAZ21haWwuY29tIiwiZXhwIjoiMTc1NzU4NDQ4MyJ9.tl6o_490NmrJqHYp8a23bhHiWVEgrASpTAxNA8ZVCII HTTP/1.1" 200 OK
INFO:     172.70.208.55:0 - "POST /mcp?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrb2xkYXNvdjNAZ21haWwuY29tIiwiZXhwIjoiMTc1NzU4NDQ4MyJ9.tl6o_490NmrJqHYp8a23bhHiWVEgrASpTAxNA8ZVCII HTTP/1.1" 307 Temporary Redirect
INFO:     172.68.44.141:0 - "POST /mcp/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrb2xkYXNvdjNAZ21haWwuY29tIiwiZXhwIjoiMTc1NzU4NDQ4MyJ9.tl6o_490NmrJqHYp8a23bhHiWVEgrASpTAxNA8ZVCII HTTP/1.1" 202 Accepted
INFO:     172.70.208.55:0 - "GET /mcp?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrb2xkYXNvdjNAZ21haWwuY29tIiwiZXhwIjoiMTc1NzU4NDQ4MyJ9.tl6o_490NmrJqHYp8a23bhHiWVEgrASpTAxNA8ZVCII HTTP/1.1" 307 Temporary Redirect
INFO:     172.68.44.141:0 - "GET /mcp/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrb2xkYXNvdjNAZ21haWwuY29tIiwiZXhwIjoiMTc1NzU4NDQ4MyJ9.tl6o_490NmrJqHYp8a23bhHiWVEgrASpTAxNA8ZVCII HTTP/1.1" 200 OK
```

Here are the logs from the MCP server when running in docker.
```
langtools-mcp  | INFO:     172.20.0.1:55396 - "POST /mcp?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrb2xkYXNvdjNAZ21haWwuY29tIiwiZXhwIjoiMTc1NzU4NDQ4MyJ9.tl6o_490NmrJqHYp8a23bhHiWVEgrASpTAxNA8ZVCII HTTP/1.1" 307 Temporary Redirect
^[[Ilangtools-mcp  | INFO:mcp.server.streamable_http_manager:Created new transport with session ID: 2bd07086cada4c01a22935b3af1a4d0e
langtools-mcp  | INFO:     172.20.0.1:55406 - "GET /mcp/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrb2xkYXNvdjNAZ21haWwuY29tIiwiZXhwIjoiMTc1NzU4NDQ4MyJ9.tl6o_490NmrJqHYp8a23bhHiWVEgrASpTAxNA8ZVCII HTTP/1.1" 400 Bad Request
```

Inspector console logs show these errors.
```
McpError: MCP error -32001: Error POSTing to endpoint (HTTP 400): {"jsonrpc":"2.0","id":"server-error","error":{"code":-32600,"message":"Bad Request: Missing session ID"}}
    at Client._onresponse (index-BNqYF5Na.js:23140:21)
    at _transport.onmessage (index-BNqYF5Na.js:23019:14)
    at processStream (index-BNqYF5Na.js:24229:77)
```