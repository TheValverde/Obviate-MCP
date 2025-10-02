# Kanban For Agents MCP Server - Quick Start Guide

Get your Kanban MCP server up and running in minutes!

## Prerequisites

- Python 3.11 or higher
- Kanban For Agents API server running (default: http://localhost:12003)
- FastMCP CLI installed

## Quick Setup

### 1. Install Dependencies

```bash
cd test-mcp
pip install -r requirements.txt
```

### 2. Start the MCP Server

```bash
# Using FastMCP CLI (recommended)
fastmcp run server.py --transport=http --port=8001

# Or using Python directly
python server.py
```

The server will start on `http://localhost:8001/mcp/`

### 3. Test the Server

```bash
# Run the test script
python test_server.py

# Or run the example usage
python example_usage.py
```

## Configuration

### Environment Variables (Optional)

```bash
# Set custom API URL (if different from default)
export KANBAN_API_BASE_URL="http://your-api-server:12003"

# Set custom tenant ID
export DEFAULT_TENANT_ID="your-tenant-id"

# Enable debug mode
export DEBUG_MODE="true"
```

### MCP Client Configuration

Add to your MCP client configuration:

**For Viren Agent:**
```json
{
  "mcp_servers": {
    "kanban_mcp": {
      "enabled": true,
      "transport": "streamable_http",
      "url": "http://127.0.0.1:8001/mcp/",
      "description": "Kanban For Agents MCP server"
    }
  }
}
```

**For Claude Desktop:**
```json
{
  "mcpServers": {
    "kanban_mcp": {
      "command": "fastmcp",
      "args": ["run", "path/to/server.py", "--transport=http", "--port=8001"]
    }
  }
}
```

## Available Tools

### Workspace Management
- `list_workspaces()` - List all workspaces
- `create_workspace(name, description)` - Create new workspace
- `get_workspace(workspace_id)` - Get workspace details
- `update_workspace(workspace_id, name, description)` - Update workspace
- `delete_workspace(workspace_id)` - Delete workspace

### Board Management
- `list_boards(workspace_id)` - List boards in workspace
- `create_board(title, workspace_id, description)` - Create new board
- `get_board(board_id)` - Get board details
- `update_board(board_id, title, description)` - Update board
- `delete_board(board_id)` - Delete board

### Column Management
- `list_columns(board_id)` - List columns in board
- `create_column(title, board_id, description, position, color)` - Create new column
- `get_column(column_id)` - Get column details
- `update_column(column_id, title, description, color)` - Update column
- `delete_column(column_id)` - Delete column
- `reorder_column(column_id, new_position)` - Reorder column

### Card Management
- `list_cards(board_id, column_id)` - List cards with filtering
- `create_card(title, board_id, column_id, description, priority, labels, assignees)` - Create new card
- `get_card(card_id)` - Get card details
- `update_card(card_id, title, description, priority, labels, assignees)` - Update card
- `delete_card(card_id)` - Delete card
- `move_card(card_id, target_column_id, position)` - Move card to different column
- `reorder_card(card_id, new_position)` - Reorder card within column

### Utility Tools
- `get_server_info()` - Get server information and status
- `create_kanban_workflow(workspace_name, board_title, workflow_type)` - Create complete workflow

## Workflow Types

The `create_kanban_workflow` tool supports these pre-built templates:

- **standard**: To Do → In Progress → Done
- **development**: Backlog → In Development → Code Review → Testing → Done
- **marketing**: Ideas → Planning → In Progress → Review → Published
- **support**: New → In Progress → Waiting for Customer → Resolved

## Example Usage

### Create a Development Workflow

```python
# Create complete workflow with one call
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

### Create and Manage Tasks

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
    card_id=card["id"],
    target_column_id="column_789"  # Code Review column
)
```

### Multi-Agent Collaboration

```python
# Agent 1 creates task
task = create_card(
    title="Design database schema",
    board_id="board_123",
    column_id="backlog_column",
    description="Design the database schema for user management",
    priority=2,
    assignees=["agent_1"]
)

# Agent 2 picks up task
update_card(
    card_id=task["id"],
    assignees=["agent_2"]
)

# Move to in progress
move_card(
    card_id=task["id"],
    target_column_id="in_progress_column"
)
```

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure Kanban API server is running on `http://localhost:12003`
   - Check `KANBAN_API_BASE_URL` environment variable
   - Verify API server is accessible

2. **MCP Server Won't Start**
   - Check if port 8001 is available
   - Ensure all dependencies are installed
   - Check Python version (3.11+ required)

3. **Tools Return Errors**
   - Verify tenant ID is correct
   - Check API server logs for errors
   - Ensure proper authentication

### Debug Mode

Enable debug mode for detailed logging:

```bash
export DEBUG_MODE="true"
python server.py
```

### Testing

Run the test suite to verify everything works:

```bash
python test_server.py
```

## Next Steps

1. **Explore the API**: Check the full API documentation in `../docs/`
2. **Customize Workflows**: Modify workflow templates in `config.py`
3. **Integrate with AI Agents**: Use the MCP tools in your agent workflows
4. **Scale Up**: Add more boards, workspaces, and automation

## Support

- **Documentation**: Check `../docs/` for complete API documentation
- **Examples**: See `example_usage.py` for usage patterns
- **Testing**: Use `test_server.py` to verify functionality
- **Configuration**: Modify `config.py` for custom settings

## Version Information

- **MCP Server**: 1.0.0
- **API Version**: v1
- **Compatibility**: FastMCP 0.1.0+, Python 3.11+
- **Last Updated**: August 2025



