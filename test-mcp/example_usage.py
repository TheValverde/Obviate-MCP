#!/usr/bin/env python3
"""
Example usage of the Kanban For Agents MCP Server

This script demonstrates how to use the MCP server tools to create
and manage a complete Kanban workflow for AI agent task management.
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
MCP_SERVER_URL = "http://localhost:8000/mcp/"

def call_mcp_tool(tool_name: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
    """Call an MCP tool and return the result."""
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
        result = response.json()
        
        if "result" in result and result["result"].get("success"):
            return result["result"]["data"]
        else:
            print(f"❌ Error calling {tool_name}: {result}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to call {tool_name}: {str(e)}")
        return None

def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")

def print_success(message: str, data: Any = None):
    """Print a success message."""
    print(f"✅ {message}")
    if data:
        print(f"   Data: {json.dumps(data, indent=2)}")

def main():
    """Demonstrate MCP server usage with a complete workflow."""
    print("🚀 Kanban For Agents MCP Server - Example Usage")
    print("This example demonstrates creating and managing a complete workflow")
    
    # Step 1: Check server status
    print_section("Server Status")
    server_info = call_mcp_tool("get_server_info")
    if server_info:
        print_success("Server is running", {
            "name": server_info.get("name"),
            "version": server_info.get("version"),
            "api_connection": server_info.get("api_connection")
        })
    
    # Step 2: Create a development workflow
    print_section("Creating Development Workflow")
    workflow = call_mcp_tool("create_kanban_workflow", {
        "workspace_name": "AI Agent Project",
        "board_title": "Development Tasks",
        "workflow_type": "development"
    })
    
    if not workflow:
        print("❌ Failed to create workflow")
        return
    
    workspace = workflow["workspace"]
    board = workflow["board"]
    columns = workflow["columns"]
    
    print_success("Created development workflow", {
        "workspace": workspace["name"],
        "board": board["title"],
        "columns": [col["title"] for col in columns]
    })
    
    # Step 3: Create some tasks
    print_section("Creating Tasks")
    
    # Find column IDs
    backlog_col = next((col for col in columns if col["title"] == "Backlog"), None)
    dev_col = next((col for col in columns if col["title"] == "In Development"), None)
    
    if not backlog_col or not dev_col:
        print("❌ Could not find required columns")
        return
    
    # Create tasks in backlog
    tasks = []
    
    task1 = call_mcp_tool("create_card", {
        "title": "Design API endpoints",
        "board_id": board["id"],
        "column_id": backlog_col["id"],
        "description": "Design RESTful API endpoints for user management",
        "priority": 3,
        "labels": ["backend", "api"],
        "assignees": ["agent_1"]
    })
    
    if task1:
        tasks.append(task1)
        print_success("Created task: Design API endpoints")
    
    task2 = call_mcp_tool("create_card", {
        "title": "Implement authentication",
        "board_id": board["id"],
        "column_id": backlog_col["id"],
        "description": "Implement JWT-based authentication system",
        "priority": 4,
        "labels": ["backend", "security"],
        "assignees": ["agent_2"]
    })
    
    if task2:
        tasks.append(task2)
        print_success("Created task: Implement authentication")
    
    task3 = call_mcp_tool("create_card", {
        "title": "Create frontend components",
        "board_id": board["id"],
        "column_id": backlog_col["id"],
        "description": "Create React components for user interface",
        "priority": 2,
        "labels": ["frontend", "ui"],
        "assignees": ["agent_3"]
    })
    
    if task3:
        tasks.append(task3)
        print_success("Created task: Create frontend components")
    
    # Step 4: Move tasks through workflow
    print_section("Moving Tasks Through Workflow")
    
    if tasks:
        # Move first task to development
        moved_task = call_mcp_tool("move_card", {
            "card_id": task1["id"],
            "target_column_id": dev_col["id"]
        })
        
        if moved_task:
            print_success(f"Moved task '{task1['title']}' to In Development")
        
        # Update task priority
        updated_task = call_mcp_tool("update_card", {
            "card_id": task2["id"],
            "priority": 5,
            "description": "Implement JWT-based authentication system with refresh tokens"
        })
        
        if updated_task:
            print_success(f"Updated task '{task2['title']}' priority to 5")
    
    # Step 5: List current state
    print_section("Current Workflow State")
    
    # List all cards in the board
    all_cards = call_mcp_tool("list_cards", {
        "board_id": board["id"]
    })
    
    if all_cards and "items" in all_cards:
        print(f"📊 Total tasks in board: {len(all_cards['items'])}")
        
        # Group by column
        by_column = {}
        for card in all_cards["items"]:
            col_name = card.get("column", {}).get("title", "Unknown")
            if col_name not in by_column:
                by_column[col_name] = []
            by_column[col_name].append(card)
        
        for col_name, cards in by_column.items():
            print(f"\n📋 {col_name} ({len(cards)} tasks):")
            for card in cards:
                priority_emoji = "🔴" if card["priority"] >= 4 else "🟡" if card["priority"] >= 2 else "🟢"
                print(f"   {priority_emoji} {card['title']} (Priority: {card['priority']})")
    
    # Step 6: Demonstrate multi-agent collaboration
    print_section("Multi-Agent Collaboration Example")
    
    if tasks:
        # Simulate agent handoff
        print("🤖 Simulating agent handoff...")
        
        # Agent 1 completes task and hands off to Agent 2
        handoff_task = call_mcp_tool("update_card", {
            "card_id": task1["id"],
            "assignees": ["agent_2"],
            "description": "API endpoints designed. Ready for implementation by Agent 2."
        })
        
        if handoff_task:
            print_success("Agent 1 handed off task to Agent 2")
        
        # Agent 2 picks up the task
        pickup_task = call_mcp_tool("move_card", {
            "card_id": task1["id"],
            "target_column_id": dev_col["id"]
        })
        
        if pickup_task:
            print_success("Agent 2 picked up the task and moved it to development")
    
    # Step 7: Cleanup (optional)
    print_section("Workflow Summary")
    
    print("🎉 Example workflow completed successfully!")
    print(f"📁 Workspace: {workspace['name']} (ID: {workspace['id']})")
    print(f"📋 Board: {board['title']} (ID: {board['id']})")
    print(f"📊 Tasks created: {len(tasks)}")
    
    print("\n💡 Next steps:")
    print("   - Continue moving tasks through the workflow")
    print("   - Add more tasks as needed")
    print("   - Use the MCP tools to automate task management")
    print("   - Integrate with AI agents for automated workflow management")
    
    print("\n🔧 Available tools for further automation:")
    print("   - list_cards() - Get all tasks in a board or column")
    print("   - move_card() - Move tasks between columns")
    print("   - update_card() - Update task details, assignees, priority")
    print("   - create_card() - Add new tasks")
    print("   - delete_card() - Remove completed tasks")

if __name__ == "__main__":
    main()



