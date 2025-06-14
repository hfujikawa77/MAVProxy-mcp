# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the MAVProxy-mcp repository, which appears to be a new project that is likely intended to integrate MAVProxy (a MAVLink proxy system for ArduPilot) with MCP (Model Context Protocol) capabilities.

## Current State

The repository now has:
- Basic MCP server implementation with fallback support
- Package structure with pyproject.toml configuration
- Simple and robust server architecture
- Basic tools: ping and get_status
- Test framework setup
- MCP configuration in .mcp.json

## Development Environment

Based on the .gitignore file, this project is set up for Python development with support for:
- Standard Python packaging (setuptools, pip, etc.)
- Virtual environments (.venv, venv/)
- Common Python tools (mypy, pytest, ruff, etc.)
- IDE support (VS Code, PyCharm, Cursor)

## Expected Architecture

Given the repository name "MAVProxy-mcp", this project will likely:
- Integrate MAVProxy functionality with MCP protocol
- Provide MAVLink communication capabilities through MCP
- Enable AI assistants to interact with ArduPilot systems
- Bridge between drone/rover control systems and AI tools

## Development Commands

Common development commands:
- `pip install -e .` - Install package in development mode
- `python -m pytest` - Run tests
- `ruff check .` - Lint code
- `ruff format .` - Format code
- `mypy src/` - Type checking
- `python -m src.mavproxy_mcp.server` - Run MCP server directly

## Notes for Future Development

- Follow ArduPilot and MAVProxy coding conventions
- Ensure proper MAVLink message handling
- Implement appropriate safety measures for drone control
- Consider MCP protocol specifications for AI integration