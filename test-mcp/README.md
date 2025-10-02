# Kanban For Agents MCP Server

A comprehensive MCP (Model Context Protocol) server that provides tools for interacting with the Kanban For Agents API, enabling AI agents to manage workspaces, boards, columns, and cards programmatically.

## Overview

This MCP server wraps around the Kanban For Agents API and provides standardized tools for:

- **Workspace Management**: Create, list, update, and delete workspaces
- **Board Management**: Create, list, update, and delete boards with default columns
- **Column Management**: Create, list, update, delete, and reorder columns
- **Card Management**: Create, list, update, delete, move, and reorder cards
- **Workflow Automation**: Pre-built workflow templates for common use cases
- **Multi-Agent Collaboration**: Support for AI agent task management and coordination

## Features

### 🔧 Complete CRUD Operations
- Full Create, Read, Update, Delete operations for all Kanban entities
- Batch operations and filtering capabilities
- Automatic error handling and data validation

### 🎯 Workflow Templates
- **Standard**: To Do → In Progress → Done
- **Development**: Backlog → In Development → Code Review → Testing → Done
- **Marketing**: Ideas → Planning → In Progress → Review → Published
- **Support**: New → In Progress → Waiting for Customer → Resolved

### 🤖 AI Agent Optimized
- Structured data models with Pydantic validation
- Consistent error responses and status codes
- Comprehensive tool documentation for AI consumption
- Multi-agent collaboration support

### 🔒 Authentication & Security
- Tenant-based authentication support
- Configurable API endpoints and credentials
- Secure error handling without exposing sensitive data

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (optional):
```bash
export KANBAN_API_BASE_URL="http://localhost:12003"
export DEFAULT_TENANT_ID="your-tenant-id"
```

## Running the Server

### Using FastMCP CLI (Recommended)

```bash
# Run with default HTTP transport and port
fastmcp run server.py --transport=http

# Run with custom port
fastmcp run server.py --transport=http --port=12007

# Run with specific port and host
fastmcp run server.py --transport=http --port=12003 --host=127.0.0.1
```

### Using Python Directly

```bash
python server.py
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KANBAN_API_BASE_URL` | `http://localhost:12003` | Base URL of the Kanban API |
| `DEFAULT_TENANT_ID` | `default` | Default tenant ID for API requests |

### API Configuration

The server connects to the Kanban For Agents API with the following defaults:
- **Base URL**: `http://localhost:12003`
- **API Version**: `v1`
- **Authentication**: Tenant-based via `X-Tenant-ID` header

## Available Tools

### Workspace Management

#### `list_workspaces(limit: int, offset: int) -> dict`
List all workspaces for the authenticated user.

**Parameters:**
- `limit` (int, optional): Maximum number of workspaces to return (default: 100)
- `offset` (int, optional): Number of workspaces to skip (default: 0)

**Returns:**
- Dictionary containing workspace list and pagination info

#### `create_workspace(name: str, description: str) -> dict`
Create a new workspace.

**Parameters:**
- `name` (str): Workspace name (max 255 characters)
- `description` (str, optional): Workspace description (max 1000 characters)

**Returns:**
- Dictionary containing the created workspace data

#### `get_workspace(workspace_id: str) -> dict`
Get a specific workspace by ID.

**Parameters:**
- `workspace_id` (str): ID of the workspace to retrieve

**Returns:**
- Dictionary containing the workspace data

#### `update_workspace(workspace_id: str, name: str, description: str) -> dict`
Update an existing workspace.

**Parameters:**
- `workspace_id` (str): ID of the workspace to update
- `name` (str, optional): New workspace name
- `description` (str, optional): New workspace description

**Returns:**
- Dictionary containing the updated workspace data

#### `delete_workspace(workspace_id: str) -> dict`
Delete a workspace.

**Parameters:**
- `workspace_id` (str): ID of the workspace to delete

**Returns:**
- Dictionary containing deletion confirmation

### Board Management

#### `list_boards(workspace_id: str, limit: int, offset: int) -> dict`
List boards with optional workspace filtering.

**Parameters:**
- `workspace_id` (str, optional): Workspace ID to filter boards
- `limit` (int, optional): Maximum number of boards to return (default: 100)
- `offset` (int, optional): Number of boards to skip (default: 0)

**Returns:**
- Dictionary containing board list and pagination info

#### `create_board(title: str, workspace_id: str, description: str, create_default_columns: bool) -> dict`
Create a new board with optional default columns.

**Parameters:**
- `title` (str): Board title (max 255 characters)
- `workspace_id` (str): ID of the workspace to create the board in
- `description` (str, optional): Board description (max 1000 characters)
- `create_default_columns` (bool, optional): Whether to create default columns (default: true)

**Returns:**
- Dictionary containing the created board data

#### `get_board(board_id: str) -> dict`
Get a specific board by ID.

**Parameters:**
- `board_id` (str): ID of the board to retrieve

**Returns:**
- Dictionary containing the board data

#### `update_board(board_id: str, title: str, description: str) -> dict`
Update an existing board.

**Parameters:**
- `board_id` (str): ID of the board to update
- `title` (str, optional): New board title
- `description` (str, optional): New board description

**Returns:**
- Dictionary containing the updated board data

#### `delete_board(board_id: str) -> dict`
Delete a board.

**Parameters:**
- `board_id` (str): ID of the board to delete

**Returns:**
- Dictionary containing deletion confirmation

### Column Management

#### `list_columns(board_id: str, limit: int, offset: int) -> dict`
List columns with optional board filtering.

**Parameters:**
- `board_id` (str, optional): Board ID to filter columns
- `limit` (int, optional): Maximum number of columns to return (default: 100)
- `offset` (int, optional): Number of columns to skip (default: 0)

**Returns:**
- Dictionary containing column list and pagination info

#### `create_column(title: str, board_id: str, description: str, position: int, color: str) -> dict`
Create a new column in a board.

**Parameters:**
- `title` (str): Column title (max 255 characters)
- `board_id` (str): ID of the board to create the column in
- `description` (str, optional): Column description (max 1000 characters)
- `position` (int, optional): Position of the column in the board (default: 0)
- `color` (str, optional): Column color

**Returns:**
- Dictionary containing the created column data

#### `get_column(column_id: str) -> dict`
Get a specific column by ID.

**Parameters:**
- `column_id` (str): ID of the column to retrieve

**Returns:**
- Dictionary containing the column data

#### `update_column(column_id: str, title: str, description: str, color: str) -> dict`
Update an existing column.

**Parameters:**
- `column_id` (str): ID of the column to update
- `title` (str, optional): New column title
- `description` (str, optional): New column description
- `color` (str, optional): New column color

**Returns:**
- Dictionary containing the updated column data

#### `delete_column(column_id: str) -> dict`
Delete a column.

**Parameters:**
- `column_id` (str): ID of the column to delete

**Returns:**
- Dictionary containing deletion confirmation

#### `reorder_column(column_id: str, new_position: int) -> dict`
Reorder a column within its board.

**Parameters:**
- `column_id` (str): ID of the column to reorder
- `new_position` (int): New position for the column

**Returns:**
- Dictionary containing the reordered column data

### Card Management

#### `list_cards(board_id: str, column_id: str, limit: int, offset: int) -> dict`
List cards with optional filtering by board or column.

**Parameters:**
- `board_id` (str, optional): Board ID to filter cards
- `column_id` (str, optional): Column ID to filter cards
- `limit` (int, optional): Maximum number of cards to return (default: 100)
- `offset` (int, optional): Number of cards to skip (default: 0)

**Returns:**
- Dictionary containing card list and pagination info

#### `create_card(title: str, board_id: str, column_id: str, description: str, priority: int, labels: list, assignees: list) -> dict`
Create a new card.

**Parameters:**
- `title` (str): Card title (max 255 characters)
- `board_id` (str): ID of the board the card belongs to
- `column_id` (str): ID of the column to place the card in
- `description` (str, optional): Card description (max 5000 characters)
- `priority` (int, optional): Card priority (1-5, default: 1)
- `labels` (list, optional): List of card labels
- `assignees` (list, optional): List of card assignees

**Returns:**
- Dictionary containing the created card data

#### `get_card(card_id: str) -> dict`
Get a specific card by ID.

**Parameters:**
- `card_id` (str): ID of the card to retrieve

**Returns:**
- Dictionary containing the card data

#### `update_card(card_id: str, title: str, description: str, priority: int, labels: list, assignees: list) -> dict`
Update an existing card.

**Parameters:**
- `card_id` (str): ID of the card to update
- `title` (str, optional): New card title
- `description` (str, optional): New card description
- `priority` (int, optional): New card priority (1-5)
- `labels` (list, optional): New list of card labels
- `assignees` (list, optional): New list of card assignees

**Returns:**
- Dictionary containing the updated card data

#### `delete_card(card_id: str) -> dict`
Delete a card.

**Parameters:**
- `card_id` (str): ID of the card to delete

**Returns:**
- Dictionary containing deletion confirmation

#### `move_card(card_id: str, target_column_id: str, position: int) -> dict`
Move a card to a different column.

**Parameters:**
- `card_id` (str): ID of the card to move
- `target_column_id` (str): ID of the target column
- `position` (int, optional): Position within the target column

**Returns:**
- Dictionary containing the moved card data

#### `reorder_card(card_id: str, new_position: int) -> dict`
Reorder a card within its current column.

**Parameters:**
- `card_id` (str): ID of the card to reorder
- `new_position` (int): New position for the card within its column

**Returns:**
- Dictionary containing the reordered card data

### Utility Tools

#### `get_server_info() -> dict`
Get information about the Kanban MCP server and API connection.

**Returns:**
- Dictionary containing server information, API status, and available tools

#### `create_kanban_workflow(workspace_name: str, board_title: str, workflow_type: str) -> dict`
Create a complete Kanban workflow with workspace, board, and default columns.

**Parameters:**
- `workspace_name` (str): Name for the new workspace
- `board_title` (str): Title for the new board
- `workflow_type` (str, optional): Type of workflow to create (standard, development, marketing, support, default: standard)

**Returns:**
- Dictionary containing the created workflow components

## Adding to MCP Clients

### For Viren Agent (mcp.json):
```json
{
  "mcp_servers": {
    "kanban_mcp": {
      "enabled": true,
      "transport": "streamable_http",
      "url": "http://127.0.0.1:12007/mcp/",
      "description": "Kanban For Agents MCP server for workspace, board, column, and card management"
    }
  }
}
```

### For Claude Desktop (~/.claude/claude_desktop_config.json):
```json
{
  "mcpServers": {
    "kanban_mcp": {
      "command": "fastmcp",
      "args": ["run", "path/to/server.py", "--transport=http", "--port=8000"]
    }
  }
}
```

### For Cursor (~/.cursor/mcp.json):
```json
{
  "mcpServers": {
    "kanban_mcp": {
      "command": "fastmcp",
      "args": ["run", "path/to/server.py", "--transport=http", "--port=8000"]
    }
  }
}
```

## Usage Examples

### Creating a Development Workflow

```python
# Create a complete development workflow
result = create_kanban_workflow(
    workspace_name="My Project",
    board_title="Development Board",
    workflow_type="development"
)

# This creates:
# - Workspace: "My Project"
# - Board: "Development Board"
# - Columns: Backlog, In Development, Code Review, Testing, Done
```

### Managing Tasks

```python
# Create a task
card = create_card(
    title="Implement user authentication",
    board_id="board_123",
    column_id="column_456",
    description="Add JWT-based authentication to the API",
    priority=3,
    labels=["backend", "security"],
    assignees=["agent_1"]
)

# Move task to next stage
move_card(
    card_id=card["data"]["id"],
    target_column_id="column_789"  # Code Review column
)
```

### Multi-Agent Collaboration

```python
# Agent 1 creates a task
task = create_card(
    title="Design database schema",
    board_id="board_123",
    column_id="backlog_column",
    description="Design the database schema for user management",
    priority=2,
    assignees=["agent_1"]
)

# Agent 2 picks up the task
update_card(
    card_id=task["data"]["id"],
    assignees=["agent_2"]
)

# Move to in progress
move_card(
    card_id=task["data"]["id"],
    target_column_id="in_progress_column"
)
```

## Testing

Use the included test script to verify the server is working:

```bash
python test_server.py
```

This will test all available tools and verify the server responses.

## Error Handling

The server provides consistent error handling across all tools:

- **API Connection Errors**: Handled gracefully with informative error messages
- **Validation Errors**: Pydantic models ensure data validation
- **HTTP Errors**: Proper status code handling and error responses
- **Authentication Errors**: Secure error handling without exposing credentials

## Production Considerations

### Security
- Use environment variables for sensitive configuration
- Implement proper authentication and authorization
- Validate all input data
- Use HTTPS in production

### Performance
- Implement connection pooling for API requests
- Add caching for frequently accessed data
- Monitor API response times
- Use async operations for better performance

### Monitoring
- Log all API interactions
- Monitor error rates and response times
- Set up alerts for API failures
- Track tool usage patterns

## Integration

This server can be integrated with any MCP-compatible client by configuring the client to connect to:

```
http://localhost:12007/mcp/
```

The server provides a comprehensive set of tools for managing Kanban workflows, making it ideal for AI agent task management and automation.

## Support

For issues and questions:
1. Check the API documentation in the `../docs/` directory
2. Review the error messages and status codes
3. Test individual tools using the test script
4. Verify API connectivity and configuration

## Version Information

- **MCP Server Version**: 1.0.0
- **API Version**: v1
- **Compatibility**: FastMCP 0.1.0+, Python 3.11+
- **Last Updated**: August 2025 