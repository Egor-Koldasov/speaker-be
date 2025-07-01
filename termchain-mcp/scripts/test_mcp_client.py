#!/usr/bin/env python3
"""
Test client for MCP server using SSE protocol.

This script tests the MCP server's SSE endpoint by:
1. Creating an SSE connection
2. Sending an initialize message
3. Listing available tools
4. Calling the define_term tool
5. Closing the session
"""

import asyncio
import json
import sys
import uuid
from typing import Dict, Any

import aiohttp

# Configuration
SERVER_URL = "http://localhost:8082"
SSE_ENDPOINT = f"{SERVER_URL}/mcp/sse"
MESSAGE_ENDPOINT = f"{SERVER_URL}/mcp/message"

class MCPClient:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.request_id = 1
        self.session = None

    async def send_message(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a JSON-RPC message to the server."""
        if params is None:
            params = {}
            
        message = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self.request_id,
        }
        
        # Special handling for initializeSession
        if method == "mcp.initializeSession":
            message["params"]["sessionId"] = self.session_id
        else:
            message["params"]["sessionId"] = self.session_id
            
        self.request_id += 1
        
        print(f"Sending: {json.dumps(message, indent=2)}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(MESSAGE_ENDPOINT, json=message) as resp:
                response = await resp.json()
                print(f"Response: {json.dumps(response, indent=2)}")
                return response

    async def connect_sse(self):
        """Establish an SSE connection to the server."""
        self.session = aiohttp.ClientSession()
        return await self.session.get(
            f"{SSE_ENDPOINT}?sessionId={self.session_id}",
            headers={"Accept": "text/event-stream"}
        )

    async def close(self):
        """Close the client session."""
        if self.session:
            await self.session.close()

async def main():
    client = MCPClient()
    
    try:
        # 1. Initialize session
        print("\n=== Initializing session ===")
        init_response = await client.send_message("mcp.initializeSession", {
            "clientInfo": {
                "name": "MCP Test Client",
                "version": "1.0.0"
            }
        })
        
        if "error" in init_response:
            print(f"Failed to initialize session: {init_response['error']}")
            return
            
        # 2. List available tools
        print("\n=== Listing tools ===")
        tools_response = await client.send_message("mcp.listTools")
        
        if "error" in tools_response:
            print(f"Failed to list tools: {tools_response['error']}")
            return
            
        # 3. Call define_term tool
        print("\n=== Calling define_term tool ===")
        define_response = await client.send_message("mcp.callTool", {
            "toolName": "define_term",
            "parameters": {
                "term": "hello",
                "source_lang": "en",
                "target_lang": "es",
                "context": "greeting"
            }
        })
        
        if "error" in define_response:
            print(f"Tool call failed: {define_response['error']}")
            return
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
