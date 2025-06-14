"""MCP Server implementation for MAVProxy integration."""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    # Fallback basic implementation
    class FastMCP:
        def __init__(self, name: str):
            self.name = name

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MAVProxyMCPServer:
    """MCP Server for MAVProxy integration."""

    def __init__(self) -> None:
        """Initialize the MCP server."""
        if MCP_AVAILABLE:
            self.server = FastMCP("mavproxy-mcp")
            self._setup_handlers()
        else:
            self.server = None
            logger.warning("MCP library not available, running in minimal mode")
        
        self.running = False
        logger.info("MAVProxy MCP Server initialized")

    def _setup_handlers(self) -> None:
        """Set up the MCP server handlers."""
        if not self.server or not MCP_AVAILABLE:
            return

        @self.server.tool()
        async def get_status() -> str:
            """Get MAVProxy connection status."""
            status = {
                "server_running": self.running,
                "mavproxy_connected": False,
                "timestamp": asyncio.get_event_loop().time(),
                "version": "0.1.0",
            }
            return json.dumps(status, indent=2)

        @self.server.tool()
        async def ping() -> str:
            """Ping the MAVProxy MCP server to check connectivity."""
            return "Pong! MAVProxy MCP Server is running."

    def get_status_sync(self) -> Dict[str, Any]:
        """Get server status synchronously."""
        return {
            "server_running": self.running,
            "mavproxy_connected": False,
            "mcp_available": MCP_AVAILABLE,
            "version": "0.1.0",
        }

    async def start(self) -> None:
        """Start the MCP server."""
        try:
            logger.info("Starting MAVProxy MCP Server...")
            self.running = True
            
            if MCP_AVAILABLE and self.server:
                # Run the MCP server
                await self.server.run()
            else:
                # Fallback mode - just keep running
                logger.info("Running in fallback mode without full MCP support")
                while self.running:
                    await asyncio.sleep(1)
                    
        except Exception as e:
            logger.error(f"Error starting MCP server: {e}")
            self.running = False
            raise

    async def stop(self) -> None:
        """Stop the MCP server."""
        logger.info("Stopping MAVProxy MCP Server...")
        self.running = False


async def main() -> None:
    """Main entry point for the MCP server."""
    # Try to use the full MCP server, fall back to simple implementation
    try:
        server = MAVProxyMCPServer()
        logger.info("Using full MCP server implementation")
    except Exception as e:
        logger.warning(f"Full MCP server failed to initialize: {e}")
        from .simple_server import SimpleMAVProxyMCPServer
        server = SimpleMAVProxyMCPServer()
        logger.info("Using simple MCP server implementation")
    
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