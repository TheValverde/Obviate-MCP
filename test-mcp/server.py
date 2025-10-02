#!/usr/bin/env python3
"""
Kanban For Agents MCP Server

This MCP server provides tools for interacting with the Kanban For Agents API,
enabling AI agents to manage workspaces, boards, columns, and cards programmatically.

The server wraps around the Kanban API endpoints and provides standardized MCP tools
for all Kanban operations including CRUD operations, task management, and workflow automation.
"""

import os
import json
import requests
from typing import Optional, List, Dict, Any, Union
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# Import configuration
from config import (
    KANBAN_API_BASE_URL, KANBAN_API_VERSION, DEFAULT_TENANT_ID,
    MCP_SERVER_NAME, MCP_SERVER_VERSION, MCP_SERVER_DESCRIPTION, MCP_SERVER_PORT,
    WORKFLOW_TEMPLATES, get_api_headers, get_config_summary
)

# Create the MCP server instance
mcp = FastMCP(
    name=MCP_SERVER_NAME,
    instructions=MCP_SERVER_DESCRIPTION
)

# Data Models
class WorkspaceCreate(BaseModel):
    name: str = Field(..., max_length=255, description="Workspace name")
    description: Optional[str] = Field(None, max_length=1000, description="Workspace description")

class BoardCreate(BaseModel):
    title: str = Field(..., max_length=255, description="Board title")
    description: Optional[str] = Field(None, max_length=1000, description="Board description")
    workspace_id: str = Field(..., description="ID of the workspace to create the board in")
    create_default_columns: bool = Field(True, description="Whether to create default columns (To Do, In Progress, Done)")

class ColumnCreate(BaseModel):
    title: str = Field(..., max_length=255, description="Column title")
    description: Optional[str] = Field(None, max_length=1000, description="Column description")
    board_id: str = Field(..., description="ID of the board to create the column in")
    position: int = Field(0, description="Position of the column in the board")
    color: Optional[str] = Field(None, description="Column color")

class CardCreate(BaseModel):
    title: str = Field(..., max_length=255, description="Card title")
    description: Optional[str] = Field(None, max_length=5000, description="Card description")
    board_id: str = Field(..., description="ID of the board the card belongs to")
    column_id: str = Field(..., description="ID of the column to place the card in")
    priority: int = Field(1, ge=1, le=5, description="Card priority (1-5)")
    labels: List[str] = Field(default_factory=list, description="Card labels")
    assignees: List[str] = Field(default_factory=list, description="Card assignees")

class CardMove(BaseModel):
    card_id: str = Field(..., description="ID of the card to move")
    target_column_id: str = Field(..., description="ID of the target column")
    position: Optional[int] = Field(None, description="Position within the target column")

# Helper Functions
def make_api_request(method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None, additional_headers: Optional[Dict] = None) -> Dict[str, Any]:
    """Make a request to the Kanban API with proper error handling."""
    url = f"{KANBAN_API_BASE_URL}/{KANBAN_API_VERSION}/{endpoint}"
    
    headers = get_api_headers()
    if additional_headers:
        headers.update(additional_headers)
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"API request failed: {str(e)}",
            "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

# Workspace Management Tools
@mcp.tool()
def list_workspaces(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    List all workspaces for the authenticated user.
    
    Args:
        limit: Maximum number of workspaces to return (default: 100)
        offset: Number of workspaces to skip (default: 0)
        
    Returns:
        Dictionary containing workspace list and pagination info
    """
    params = {"limit": limit, "offset": offset}
    return make_api_request("GET", "workspaces/", params=params)

@mcp.tool()
def create_workspace(name: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new workspace.
    
    Args:
        name: Workspace name (max 255 characters)
        description: Optional workspace description (max 1000 characters)
        
    Returns:
        Dictionary containing the created workspace data
    """
    data = {"name": name}
    if description:
        data["description"] = description
    
    return make_api_request("POST", "workspaces/", data=data)

@mcp.tool()
def get_workspace(workspace_id: str) -> Dict[str, Any]:
    """
    Get a specific workspace by ID.
    
    Args:
        workspace_id: ID of the workspace to retrieve
        
    Returns:
        Dictionary containing the workspace data
    """
    return make_api_request("GET", f"workspaces/{workspace_id}")

@mcp.tool()
def update_workspace(workspace_id: str, name: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Update an existing workspace.
    
    Args:
        workspace_id: ID of the workspace to update
        name: New workspace name (optional)
        description: New workspace description (optional)
        
    Returns:
        Dictionary containing the updated workspace data
    """
    data = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    
    return make_api_request("PUT", f"workspaces/{workspace_id}", data=data)

@mcp.tool()
def delete_workspace(workspace_id: str) -> Dict[str, Any]:
    """
    Delete a workspace.
    
    Args:
        workspace_id: ID of the workspace to delete
        
    Returns:
        Dictionary containing deletion confirmation
    """
    return make_api_request("DELETE", f"workspaces/{workspace_id}")

# Board Management Tools
@mcp.tool()
def list_boards(workspace_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    List boards with optional workspace filtering.
    
    Args:
        workspace_id: Optional workspace ID to filter boards
        limit: Maximum number of boards to return (default: 100)
        offset: Number of boards to skip (default: 0)
        
    Returns:
        Dictionary containing board list and pagination info
    """
    params = {"limit": limit, "offset": offset}
    if workspace_id:
        params["workspace_id"] = workspace_id
    
    return make_api_request("GET", "boards/", params=params)

@mcp.tool()
def create_board(title: str, workspace_id: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new board.
    
    Args:
        title: Board name (max 255 characters) - will be sent as "name" to API
        workspace_id: ID of the workspace to create the board in
        description: Optional board description (max 1000 characters)
        
    Returns:
        Dictionary containing the created board data
    """
    data = {
        "name": title,  # Changed from "title" to "name" to match Swagger docs
        "workspace_id": workspace_id,
        "template": {},  # Add template field as per Swagger docs
        "meta_data": {}  # Add meta_data field as per Swagger docs
    }
    if description:
        data["description"] = description
    
    return make_api_request("POST", "boards/", data=data)

@mcp.tool()
def get_board(board_id: str) -> Dict[str, Any]:
    """
    Get a specific board by ID.
    
    Args:
        board_id: ID of the board to retrieve
        
    Returns:
        Dictionary containing the board data
    """
    return make_api_request("GET", f"boards/{board_id}")

@mcp.tool()
def update_board(board_id: str, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Update an existing board.
    
    Args:
        board_id: ID of the board to update
        title: New board title (optional)
        description: New board description (optional)
        
    Returns:
        Dictionary containing the updated board data
    """
    data = {}
    if title is not None:
        data["title"] = title
    if description is not None:
        data["description"] = description
    
    return make_api_request("PUT", f"boards/{board_id}", data=data)

@mcp.tool()
def delete_board(board_id: str) -> Dict[str, Any]:
    """
    Delete a board.
    
    Args:
        board_id: ID of the board to delete
        
    Returns:
        Dictionary containing deletion confirmation
    """
    return make_api_request("DELETE", f"boards/{board_id}")

# Column Management Tools
@mcp.tool()
def list_columns(board_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    List columns with optional board filtering.
    Do not truncate any IDs.
    
    Args:
        board_id: Optional board ID to filter columns
        limit: Maximum number of columns to return (default: 100)
        offset: Number of columns to skip (default: 0)
        
    Returns:
        Dictionary containing column list and pagination info
    """
    if board_id:
        # Use correct endpoint from Swagger docs: GET /v1/boards/{board_id}/columns
        params = {"limit": limit, "offset": offset}
        return make_api_request("GET", f"boards/{board_id}/columns", params=params)
    else:
        params = {"limit": limit, "offset": offset}
        return make_api_request("GET", "columns/", params=params)

@mcp.tool()
def create_column(title: str, board_id: str, description: Optional[str] = None, position: int = 0, color: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new column in a board.
    
    Args:
        title: Column title (max 255 characters)
        board_id: ID of the board to create the column in
        description: Optional column description (max 1000 characters)
        position: Position of the column in the board (default: 0)
        color: Optional column color
        
    Returns:
        Dictionary containing the created column data
    """
    data = {
        "name": title,  # Changed from "title" to "name" to match API
        "board_id": board_id,
        "position": position
    }
    if description:
        data["description"] = description
    if color:
        data["color"] = color
    
    return make_api_request("POST", "columns/", data=data)

@mcp.tool()
def get_column(column_id: str) -> Dict[str, Any]:
    """
    Get a specific column by ID.
    
    Args:
        column_id: ID of the column to retrieve
        
    Returns:
        Dictionary containing the column data
    """
    return make_api_request("GET", f"columns/{column_id}")

@mcp.tool()
def update_column(column_id: str, title: Optional[str] = None, description: Optional[str] = None, color: Optional[str] = None) -> Dict[str, Any]:
    """
    Update an existing column.
    
    Args:
        column_id: ID of the column to update
        title: New column title (optional)
        description: New column description (optional)
        color: New column color (optional)
        
    Returns:
        Dictionary containing the updated column data
    """
    data = {}
    if title is not None:
        data["title"] = title
    if description is not None:
        data["description"] = description
    if color is not None:
        data["color"] = color
    
    return make_api_request("PUT", f"columns/{column_id}", data=data)

@mcp.tool()
def delete_column(column_id: str) -> Dict[str, Any]:
    """
    Delete a column.
    
    Args:
        column_id: ID of the column to delete
        
    Returns:
        Dictionary containing deletion confirmation
    """
    return make_api_request("DELETE", f"columns/{column_id}")

@mcp.tool()
def reorder_column(column_id: str, new_position: int) -> Dict[str, Any]:
    """
    Reorder a column within its board.
    
    Args:
        column_id: ID of the column to reorder
        new_position: New position for the column
        
    Returns:
        Dictionary containing the reordered column data
    """
    # Use URL query parameters directly in URL string (as per test script)
    url = f"columns/{column_id}/reorder?new_position={new_position}"
    
    return make_api_request("POST", url)

# Card Management Tools
@mcp.tool()
def list_cards(board_id: Optional[str] = None, column_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    List cards with optional filtering by board or column.
    Do not truncate any IDs.

    Args:
        board_id: Optional board ID to filter cards
        column_id: Optional column ID to filter cards
        limit: Maximum number of cards to return (default: 100)
        offset: Number of cards to skip (default: 0)
        
    Returns:
        Dictionary containing card list and pagination info
    """
    if column_id:
        params = {"column_id": column_id, "limit": limit, "offset": offset}
        return make_api_request("GET", "cards/", params=params)
    elif board_id:
        params = {"board_id": board_id, "limit": limit, "offset": offset}
        return make_api_request("GET", "cards/", params=params)
    else:
        params = {"limit": limit, "offset": offset}
        return make_api_request("GET", "cards/", params=params)

@mcp.tool()
def create_card(title: str, board_id: str, column_id: str, description: Optional[str] = None, priority: int = 1, labels: Optional[List[str]] = None, assignees: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Create a new card.
    
    Args:
        title: Card title (max 255 characters)
        board_id: ID of the board the card belongs to
        column_id: ID of the column to place the card in
        description: Optional card description (max 5000 characters)
        priority: Card priority (1-5, default: 1)
        labels: Optional list of card labels
        assignees: Optional list of card assignees
        
    Returns:
        Dictionary containing the created card data
    """
    data = {
        "title": title,
        "description": description or "",
        "board_id": board_id,
        "column_id": column_id,
        "position": 0,
        "priority": priority,
        "labels": labels or [],
        "assignees": assignees or [],
        "agent_context": {},
        "workflow_state": {},
        "fields": {},
        "meta_data": {}
    }
    
    return make_api_request("POST", "cards/", data=data)

@mcp.tool()
def get_card(card_id: str) -> Dict[str, Any]:
    """
    Get a specific card by ID.
    
    Args:
        card_id: ID of the card to retrieve
        
    Returns:
        Dictionary containing the card data
    """
    return make_api_request("GET", f"cards/{card_id}")

@mcp.tool()
def update_card(card_id: str, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[int] = None, labels: Optional[List[str]] = None, assignees: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Update an existing card.
    
    Args:
        card_id: ID of the card to update
        title: New card title (optional)
        description: New card description (optional)
        priority: New card priority (1-5, optional)
        labels: New list of card labels (optional)
        assignees: New list of card assignees (optional)
        
    Returns:
        Dictionary containing the updated card data
    """
    # First get the current card to get its full data and version for optimistic concurrency
    current_card = make_api_request("GET", f"cards/{card_id}")
    if not current_card.get("success", True):  # Handle both success=True and no success field
        return current_card
    
    current_version = current_card.get("version", 1)
    
    # Start with current card data and update only the fields that are provided
    data = {
        "title": current_card.get("title", ""),
        "description": current_card.get("description", ""),
        "column_id": current_card.get("column_id", ""),
        "position": current_card.get("position", 0),
        "priority": current_card.get("priority", 1),
        "labels": current_card.get("labels", []),
        "assignees": current_card.get("assignees", [])
    }
    
    # Update only the fields that are provided
    if title is not None:
        data["title"] = title
    if description is not None:
        data["description"] = description
    if priority is not None:
        data["priority"] = priority
    if labels is not None:
        data["labels"] = labels
    if assignees is not None:
        data["assignees"] = assignees
    
    # Add If-Match header with version "1" for optimistic concurrency control
    additional_headers = {"If-Match": "1"}
    
    return make_api_request("PUT", f"cards/{card_id}", data=data, additional_headers=additional_headers)

@mcp.tool()
def delete_card(card_id: str) -> Dict[str, Any]:
    """
    Delete a card (soft delete).
    
    Args:
        card_id: ID of the card to delete
        
    Returns:
        Dictionary containing deletion confirmation
    """
    return make_api_request("DELETE", f"cards/{card_id}")

@mcp.tool()
def move_card(card_id: str, target_column_id: str, position: Optional[int] = None) -> Dict[str, Any]:
    """
    Move a card to a different column.
    
    Args:
        card_id: ID of the card to move
        target_column_id: ID of the target column
        position: Optional position within the target column
        
    Returns:
        Dictionary containing the moved card data
    """
    # Use URL query parameters directly in the URL string (as per test script)
    url = f"cards/{card_id}/move?column_id={target_column_id}"
    if position is not None:
        url += f"&position={position}"
    else:
        url += "&position=0"
    
    return make_api_request("POST", url)

@mcp.tool()
def reorder_card(card_id: str, new_position: int) -> Dict[str, Any]:
    """
    Reorder a card within its current column.
    
    Args:
        card_id: ID of the card to reorder
        new_position: New position for the card within its column
        
    Returns:
        Dictionary containing the reordered card data
    """
    # Use URL query parameters directly in the URL string (as per test script)
    url = f"cards/{card_id}/reorder?new_position={new_position}"
    
    return make_api_request("POST", url)

# Utility Tools
@mcp.tool()
def get_server_info() -> Dict[str, Any]:
    """
    Get information about the Kanban MCP server and API connection.
    
    Returns:
        Dictionary containing server information and API status
    """
    # Test API connection
    api_status = make_api_request("GET", "workspaces/", params={"limit": 1})
    
    # Get configuration summary
    config_summary = get_config_summary()
    
    return {
        "name": MCP_SERVER_NAME,
        "version": MCP_SERVER_VERSION,
        "description": "MCP server for managing Kanban boards, workspaces, columns, and cards",
        "api_base_url": KANBAN_API_BASE_URL,
        "api_version": KANBAN_API_VERSION,
        "tenant_id": DEFAULT_TENANT_ID,
        "api_connection": "connected" if api_status.get("success", False) else "disconnected",
        "tools_available": [
            # Workspace tools
            "list_workspaces", "create_workspace", "get_workspace", "update_workspace", "delete_workspace",
            # Board tools
            "list_boards", "create_board", "get_board", "update_board", "delete_board",
            # Column tools
            "list_columns", "create_column", "get_column", "update_column", "delete_column", "reorder_column",
            # Card tools
            "list_cards", "create_card", "get_card", "update_card", "delete_card", "move_card", "reorder_card",
            # Utility tools
            "get_server_info", "create_kanban_workflow"
        ],
        "status": "running",
        "configuration": config_summary
    }

@mcp.tool()
def get_server_config() -> Dict[str, Any]:
    """
    Get detailed configuration information for the Kanban MCP server.
    
    Returns:
        Dictionary containing all configuration settings and options
    """
    return get_config_summary()

@mcp.tool()
def create_kanban_workflow(workspace_name: str, board_title: str, workflow_type: str = "standard") -> Dict[str, Any]:
    """
    Create a complete Kanban workflow with workspace, board, and default columns.
    
    Args:
        workspace_name: Name for the new workspace
        board_title: Title for the new board
        workflow_type: Type of workflow to create (standard, development, marketing, support)
        
    Returns:
        Dictionary containing the created workflow components
    """
    # Use workflow templates from config
    workflow_templates = WORKFLOW_TEMPLATES
    
    # Create workspace
    workspace_result = create_workspace(workspace_name)
    if not workspace_result.get("success", False):
        return {"success": False, "error": f"Failed to create workspace: {workspace_result.get('error', 'Unknown error')}"}
    
    workspace_id = workspace_result["data"]["id"]
    
    # Create board
    board_result = create_board(board_title, workspace_id, create_default_columns=False)
    if not board_result.get("success", False):
        return {"success": False, "error": f"Failed to create board: {board_result.get('error', 'Unknown error')}"}
    
    board_id = board_result["data"]["id"]
    
    # Create columns based on template
    template = workflow_templates.get(workflow_type, workflow_templates["standard"])
    columns = []
    
    for i, column_data in enumerate(template):
        column_result = create_column(
            title=column_data["title"],
            board_id=board_id,
            description=column_data["description"],
            position=i,
            color=column_data["color"]
        )
        if column_result.get("success", False):
            columns.append(column_result["data"])
    
    return {
        "success": True,
        "workflow": {
            "workspace": workspace_result["data"],
            "board": board_result["data"],
            "columns": columns,
            "workflow_type": workflow_type
        }
    }

if __name__ == "__main__":
    print("Starting Kanban For Agents MCP Server...")
    print("Available tools:")
    print("\nWorkspace Management:")
    print("- list_workspaces(limit: int, offset: int) -> dict")
    print("- create_workspace(name: str, description: str) -> dict")
    print("- get_workspace(workspace_id: str) -> dict")
    print("- update_workspace(workspace_id: str, name: str, description: str) -> dict")
    print("- delete_workspace(workspace_id: str) -> dict")
    
    print("\nBoard Management:")
    print("- list_boards(workspace_id: str, limit: int, offset: int) -> dict")
    print("- create_board(title: str, workspace_id: str, description: str, create_default_columns: bool) -> dict")
    print("- get_board(board_id: str) -> dict")
    print("- update_board(board_id: str, title: str, description: str) -> dict")
    print("- delete_board(board_id: str) -> dict")
    
    print("\nColumn Management:")
    print("- list_columns(board_id: str, limit: int, offset: int) -> dict")
    print("- create_column(title: str, board_id: str, description: str, position: int, color: str) -> dict")
    print("- get_column(column_id: str) -> dict")
    print("- update_column(column_id: str, title: str, description: str, color: str) -> dict")
    print("- delete_column(column_id: str) -> dict")
    print("- reorder_column(column_id: str, new_position: int) -> dict")
    
    print("\nCard Management:")
    print("- list_cards(board_id: str, column_id: str, limit: int, offset: int) -> dict")
    print("- create_card(title: str, board_id: str, column_id: str, description: str, priority: int, labels: list, assignees: list) -> dict")
    print("- get_card(card_id: str) -> dict")
    print("- update_card(card_id: str, title: str, description: str, priority: int, labels: list, assignees: list) -> dict")
    print("- delete_card(card_id: str) -> dict")
    print("- move_card(card_id: str, target_column_id: str, position: int) -> dict")
    print("- reorder_card(card_id: str, new_position: int) -> dict")
    
    print("\nUtility Tools:")
    print("- get_server_info() -> dict")
    print("- get_server_config() -> dict")
    print("- create_kanban_workflow(workspace_name: str, board_title: str, workflow_type: str) -> dict")
    
    print(f"\nAPI Configuration:")
    print(f"- Base URL: {KANBAN_API_BASE_URL}")
    print(f"- API Version: {KANBAN_API_VERSION}")
    print(f"- Tenant ID: {DEFAULT_TENANT_ID}")
    
    print("\nServer is ready!")
    
    # Run the server with default streamable_http transport
    mcp.run(transport="http", port=MCP_SERVER_PORT, host="0.0.0.0") 