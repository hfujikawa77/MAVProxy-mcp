"""Simple MCP Server implementation for MAVProxy integration."""

import asyncio
import json
import logging
import sys
from typing import Any, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleMAVProxyMCPServer:
    """Simple MCP Server for MAVProxy integration."""

    def __init__(self) -> None:
        """Initialize the simple MCP server."""
        self.running = False
        self.tools = {
            "get_status": self._get_status,
            "ping": self._ping,
        }
        logger.info("Simple MAVProxy MCP Server initialized")

    async def _get_status(self, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get MAVProxy connection status."""
        return {
            "server_running": self.running,
            "mavproxy_connected": False,
            "version": "0.1.0",
            "tools_available": list(self.tools.keys()),
        }

    async def _ping(self, args: Dict[str, Any] = None) -> str:
        """Ping the MAVProxy MCP server to check connectivity."""
        return "Pong! MAVProxy MCP Server is running."

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests."""
        try:
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "tools/list":
                return {
                    "tools": [
                        {
                            "name": "get_status",
                            "description": "Get MAVProxy connection status",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": [],
                            },
                        },
                        {
                            "name": "ping", 
                            "description": "Ping the MAVProxy MCP server to check connectivity",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": [],
                            },
                        },
                    ]
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                
                if tool_name in self.tools:
                    result = await self.tools[tool_name](tool_args)
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result) if isinstance(result, dict) else str(result)
                            }
                        ]
                    }
                else:
                    return {
                        "error": f"Unknown tool: {tool_name}",
                        "isError": True
                    }
            else:
                return {
                    "error": f"Unknown method: {method}",
                    "isError": True
                }
                
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "error": str(e),
                "isError": True
            }

    async def start(self) -> None:
        """Start the simple MCP server."""
        try:
            logger.info("Starting Simple MAVProxy MCP Server...")
            self.running = True
            
            # Simple server loop - in a real implementation this would
            # handle stdio or network communication
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error starting server: {e}")
            self.running = False
            raise

    async def stop(self) -> None:
        """Stop the simple MCP server."""
        logger.info("Stopping Simple MAVProxy MCP Server...")
        self.running = False

    def get_status_sync(self) -> Dict[str, Any]:
        """Get server status synchronously."""
        return {
            "server_running": self.running,
            "mavproxy_connected": False,
            "version": "0.1.0",
            "implementation": "simple",
        }


async def main() -> None:
    """Main entry point for the simple MCP server."""
    server = SimpleMAVProxyMCPServer()
    
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
    finally:
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())