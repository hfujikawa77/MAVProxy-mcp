# MAVProxy MCP Server

MAVProxy MCP (Model Context Protocol) Server enables AI assistants to interact with ArduPilot systems through MAVProxy.

## Features

- MCP server implementation for MAVProxy integration
- Basic tool support (ping, status)
- Asynchronous operation
- Error handling and logging
- Type checking with mypy
- Code formatting with ruff

## Installation

```bash
pip install -e .
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

Start the MCP server:

```bash
mavproxy-mcp
```

## Testing

Run tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=mavproxy_mcp
```

## Code Quality

Format code:

```bash
ruff format .
```

Lint code:

```bash
ruff check .
```

Type check:

```bash
mypy src/
```

## License

MIT License