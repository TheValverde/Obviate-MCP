#!/usr/bin/env python3
"""
Test script for the Kanban For Agents MCP Server

This script tests all available tools in the Kanban MCP server to verify
functionality and API connectivity.
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
MCP_SERVER_URL = "http://localhost:12008/mcp/"
KANBAN_API_BASE_URL = "http://localhost:12003"

def test_mcp_tool(tool_name: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test a specific MCP tool by making a request to the server."""
    if args is None:
        args = {}
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": args
        }
    }
    
    try:
        response = requests.post(MCP_SERVER_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

def test_kanban_api_connection() -> bool:
    """Test if the Kanban API is accessible."""
    try:
        response = requests.get(f"{KANBAN_API_BASE_URL}/v1/workspaces/", timeout=10)
        return response.status_code == 200
    except:
        return False

def print_test_result(test_name: str, result: Dict[str, Any], expected_success: bool = True):
    """Print test results in a formatted way."""
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print(f"{'='*60}")
    
    if "error" in result:
        print(f"❌ FAILED: {result['error']}")
        return False
    
    if "result" in result:
        result_data = result["result"]
        if isinstance(result_data, dict) and result_data.get("success") == expected_success:
            print(f"✅ SUCCESS")
            if "data" in result_data:
                print(f"Data: {json.dumps(result_data['data'], indent=2)}")
            return True
        else:
            print(f"❌ FAILED: Unexpected result")
            print(f"Result: {json.dumps(result_data, indent=2)}")
            return False
    else:
        print(f"❌ FAILED: No result in response")
        print(f"Response: {json.dumps(result, indent=2)}")
        return False

def main():
    """Run all tests for the Kanban MCP server."""
    print("🧪 Testing Kanban For Agents MCP Server")
    print("=" * 60)
    
    # Test API connection first
    print("\n🔗 Testing Kanban API Connection...")
    if not test_kanban_api_connection():
        print("❌ Kanban API is not accessible. Please ensure the API server is running.")
        print(f"   Expected URL: {KANBAN_API_BASE_URL}")
        return
    
    print("✅ Kanban API is accessible")
    
    # Test server info
    print_test_result("get_server_info", test_mcp_tool("get_server_info"))
    
    # Test workspace management
    print_test_result("list_workspaces", test_mcp_tool("list_workspaces", {"limit": 5}))
    
    # Create a test workspace
    workspace_result = test_mcp_tool("create_workspace", {
        "name": "Test Workspace",
        "description": "Workspace for testing MCP server"
    })
    
    if print_test_result("create_workspace", workspace_result):
        workspace_id = workspace_result["result"]["data"]["id"]
        print(f"Created workspace ID: {workspace_id}")
        
        # Test getting the workspace
        print_test_result("get_workspace", test_mcp_tool("get_workspace", {"workspace_id": workspace_id}))
        
        # Test board management
        board_result = test_mcp_tool("create_board", {
            "title": "Test Board",
            "workspace_id": workspace_id,
            "description": "Board for testing MCP server",
            "create_default_columns": True
        })
        
        if print_test_result("create_board", board_result):
            board_id = board_result["result"]["data"]["id"]
            print(f"Created board ID: {board_id}")
            
            # Test getting the board
            print_test_result("get_board", test_mcp_tool("get_board", {"board_id": board_id}))
            
            # Test listing boards
            print_test_result("list_boards", test_mcp_tool("list_boards", {"workspace_id": workspace_id}))
            
            # Test column management
            column_result = test_mcp_tool("create_column", {
                "title": "Test Column",
                "board_id": board_id,
                "description": "Column for testing",
                "position": 0,
                "color": "#ff0000"
            })
            
            if print_test_result("create_column", column_result):
                column_id = column_result["result"]["data"]["id"]
                print(f"Created column ID: {column_id}")
                
                # Test getting the column
                print_test_result("get_column", test_mcp_tool("get_column", {"column_id": column_id}))
                
                # Test listing columns
                print_test_result("list_columns", test_mcp_tool("list_columns", {"board_id": board_id}))
                
                # Test card management
                card_result = test_mcp_tool("create_card", {
                    "title": "Test Card",
                    "board_id": board_id,
                    "column_id": column_id,
                    "description": "Card for testing MCP server",
                    "priority": 3,
                    "labels": ["test", "mcp"],
                    "assignees": ["test-agent"]
                })
                
                if print_test_result("create_card", card_result):
                    card_id = card_result["result"]["data"]["id"]
                    print(f"Created card ID: {card_id}")
                    
                    # Test getting the card
                    print_test_result("get_card", test_mcp_tool("get_card", {"card_id": card_id}))
                    
                    # Test listing cards
                    print_test_result("list_cards", test_mcp_tool("list_cards", {"board_id": board_id}))
                    print_test_result("list_cards by column", test_mcp_tool("list_cards", {"column_id": column_id}))
                    
                    # Test updating the card
                    update_result = test_mcp_tool("update_card", {
                        "card_id": card_id,
                        "title": "Updated Test Card",
                        "priority": 4
                    })
                    print_test_result("update_card", update_result)
                    
                    # Test moving the card (if there are other columns)
                    columns_result = test_mcp_tool("list_columns", {"board_id": board_id})
                    if columns_result.get("result", {}).get("data", {}).get("items"):
                        other_columns = [col for col in columns_result["result"]["data"]["items"] if col["id"] != column_id]
                        if other_columns:
                            target_column_id = other_columns[0]["id"]
                            move_result = test_mcp_tool("move_card", {
                                "card_id": card_id,
                                "target_column_id": target_column_id
                            })
                            print_test_result("move_card", move_result)
                    
                    # Test reordering the card
                    reorder_result = test_mcp_tool("reorder_card", {
                        "card_id": card_id,
                        "new_position": 0
                    })
                    print_test_result("reorder_card", reorder_result)
                    
                    # Clean up - delete the card
                    print_test_result("delete_card", test_mcp_tool("delete_card", {"card_id": card_id}))
                
                # Test reordering the column
                reorder_column_result = test_mcp_tool("reorder_column", {
                    "column_id": column_id,
                    "new_position": 1
                })
                print_test_result("reorder_column", reorder_column_result)
                
                # Clean up - delete the column
                print_test_result("delete_column", test_mcp_tool("delete_column", {"column_id": column_id}))
            
            # Clean up - delete the board
            print_test_result("delete_board", test_mcp_tool("delete_board", {"board_id": board_id}))
        
        # Test updating the workspace
        update_workspace_result = test_mcp_tool("update_workspace", {
            "workspace_id": workspace_id,
            "name": "Updated Test Workspace"
        })
        print_test_result("update_workspace", update_workspace_result)
        
        # Clean up - delete the workspace
        print_test_result("delete_workspace", test_mcp_tool("delete_workspace", {"workspace_id": workspace_id}))
    
    # Test workflow creation
    workflow_result = test_mcp_tool("create_kanban_workflow", {
        "workspace_name": "Workflow Test Workspace",
        "board_title": "Workflow Test Board",
        "workflow_type": "development"
    })
    
    if print_test_result("create_kanban_workflow", workflow_result):
        workflow_data = workflow_result["result"]["data"]["workflow"]
        workspace_id = workflow_data["workspace"]["id"]
        board_id = workflow_data["board"]["id"]
        
        print(f"Created workflow:")
        print(f"  Workspace: {workflow_data['workspace']['name']} (ID: {workspace_id})")
        print(f"  Board: {workflow_data['board']['title']} (ID: {board_id})")
        print(f"  Columns: {len(workflow_data['columns'])} columns created")
        
        # Clean up the workflow
        print_test_result("delete_board", test_mcp_tool("delete_board", {"board_id": board_id}))
        print_test_result("delete_workspace", test_mcp_tool("delete_workspace", {"workspace_id": workspace_id}))
    
    print("\n" + "="*60)
    print("🎉 All tests completed!")
    print("="*60)

if __name__ == "__main__":
    main() 