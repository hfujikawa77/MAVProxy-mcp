"""Tests for MAVProxy MCP Server."""

import pytest
from unittest.mock import AsyncMock, patch

from mavproxy_mcp.simple_server import SimpleMAVProxyMCPServer


class TestSimpleMAVProxyMCPServer:
    """Test cases for SimpleMAVProxyMCPServer."""

    @pytest.fixture
    def server(self) -> SimpleMAVProxyMCPServer:
        """Create a server instance for testing."""
        return SimpleMAVProxyMCPServer()

    def test_server_initialization(self, server: SimpleMAVProxyMCPServer) -> None:
        """Test server initialization."""
        assert server.tools is not None
        assert "ping" in server.tools
        assert "get_status" in server.tools

    @pytest.mark.asyncio
    async def test_ping_tool(self, server: SimpleMAVProxyMCPServer) -> None:
        """Test ping tool."""
        result = await server._ping()
        assert result == "Pong! MAVProxy MCP Server is running."

    @pytest.mark.asyncio
    async def test_get_status_tool(self, server: SimpleMAVProxyMCPServer) -> None:
        """Test get_status tool."""
        result = await server._get_status()
        assert isinstance(result, dict)
        assert "server_running" in result
        assert "version" in result
        assert result["version"] == "0.1.0"

    @pytest.mark.asyncio
    async def test_handle_tools_list_request(self, server: SimpleMAVProxyMCPServer) -> None:
        """Test tools list request handling."""
        request = {"method": "tools/list", "params": {}}
        result = await server.handle_request(request)
        
        assert "tools" in result
        assert len(result["tools"]) == 2
        tool_names = [tool["name"] for tool in result["tools"]]
        assert "ping" in tool_names
        assert "get_status" in tool_names

    @pytest.mark.asyncio
    async def test_handle_tools_call_request(self, server: SimpleMAVProxyMCPServer) -> None:
        """Test tools call request handling."""
        request = {
            "method": "tools/call",
            "params": {
                "name": "ping",
                "arguments": {}
            }
        }
        result = await server.handle_request(request)
        
        assert "content" in result
        assert len(result["content"]) == 1
        assert "Pong!" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_handle_unknown_tool_request(self, server: SimpleMAVProxyMCPServer) -> None:
        """Test unknown tool request handling."""
        request = {
            "method": "tools/call",
            "params": {
                "name": "unknown_tool",
                "arguments": {}
            }
        }
        result = await server.handle_request(request)
        
        assert "error" in result
        assert result["isError"] is True

    @pytest.mark.asyncio 
    async def test_server_stop(self, server: SimpleMAVProxyMCPServer) -> None:
        """Test server stop functionality."""
        # Should not raise any exceptions
        await server.stop()
        assert server.running is False

    def test_get_status_sync(self, server: SimpleMAVProxyMCPServer) -> None:
        """Test synchronous status retrieval."""
        status = server.get_status_sync()
        assert isinstance(status, dict)
        assert "server_running" in status
        assert "implementation" in status
        assert status["implementation"] == "simple"