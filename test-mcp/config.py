#!/usr/bin/env python3
"""
Configuration file for the Kanban For Agents MCP Server

This file contains all configuration settings for the MCP server,
including API endpoints, authentication, and server behavior.
"""

import os
from typing import Dict, Any

# API Configuration
KANBAN_API_BASE_URL = os.getenv("KANBAN_API_BASE_URL", "http://localhost:12003")
KANBAN_API_VERSION = os.getenv("KANBAN_API_VERSION", "v1")
DEFAULT_TENANT_ID = os.getenv("DEFAULT_TENANT_ID", "default")

# MCP Server Configuration
MCP_SERVER_NAME = "Kanban For Agents MCP Server"
MCP_SERVER_VERSION = "1.0.0"
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "12007"))
MCP_SERVER_DESCRIPTION = """
This MCP server provides comprehensive tools for managing Kanban boards, workspaces, columns, and cards.

Available operations:
- Workspace management (create, list, update, delete workspaces)
- Board management (create, list, update, delete boards)
- Column management (create, list, update, delete columns)
- Card management (create, list, update, delete, move cards)
- Task workflow automation
- Multi-agent collaboration support

All tools handle authentication, error handling, and data transformation automatically.
Use these tools to create and manage Kanban workflows for AI agent task management.
"""

# Workflow Templates
WORKFLOW_TEMPLATES = {
    "standard": [
        {"title": "To Do", "description": "Tasks to be started", "color": "#e3e3e3"},
        {"title": "In Progress", "description": "Tasks currently being worked on", "color": "#ffd700"},
        {"title": "Done", "description": "Completed tasks", "color": "#90ee90"}
    ],
    "development": [
        {"title": "Backlog", "description": "Features and tasks to be implemented", "color": "#e3e3e3"},
        {"title": "In Development", "description": "Currently being developed", "color": "#ffd700"},
        {"title": "Code Review", "description": "Ready for code review", "color": "#ffa500"},
        {"title": "Testing", "description": "In testing phase", "color": "#87ceeb"},
        {"title": "Done", "description": "Completed and deployed", "color": "#90ee90"}
    ],
    "marketing": [
        {"title": "Ideas", "description": "Marketing ideas and concepts", "color": "#e3e3e3"},
        {"title": "Planning", "description": "Campaign planning and strategy", "color": "#ffd700"},
        {"title": "In Progress", "description": "Campaigns being executed", "color": "#ffa500"},
        {"title": "Review", "description": "Content review and approval", "color": "#87ceeb"},
        {"title": "Published", "description": "Published and live", "color": "#90ee90"}
    ],
    "support": [
        {"title": "New", "description": "New support requests", "color": "#e3e3e3"},
        {"title": "In Progress", "description": "Being worked on", "color": "#ffd700"},
        {"title": "Waiting for Customer", "description": "Waiting for customer response", "color": "#ffa500"},
        {"title": "Resolved", "description": "Issues resolved", "color": "#90ee90"}
    ]
}

# API Headers
def get_api_headers() -> Dict[str, str]:
    """Get the standard headers for API requests."""
    return {
        "Content-Type": "application/json",
        "X-Tenant-ID": DEFAULT_TENANT_ID
    }

# Validation Settings
MAX_TITLE_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 1000
MAX_CARD_DESCRIPTION_LENGTH = 5000
MIN_PRIORITY = 1
MAX_PRIORITY = 5

# Pagination Defaults
DEFAULT_LIMIT = 100
DEFAULT_OFFSET = 0
MAX_LIMIT = 1000

# Error Messages
ERROR_MESSAGES = {
    "api_connection_failed": "Failed to connect to Kanban API",
    "invalid_workspace_id": "Invalid workspace ID provided",
    "invalid_board_id": "Invalid board ID provided",
    "invalid_column_id": "Invalid column ID provided",
    "invalid_card_id": "Invalid card ID provided",
    "validation_error": "Data validation failed",
    "permission_denied": "Permission denied for this operation",
    "not_found": "Resource not found",
    "server_error": "Internal server error"
}

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Performance Settings
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = float(os.getenv("RETRY_DELAY", "1.0"))

# Security Settings
ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "true").lower() == "true"
LOG_SENSITIVE_DATA = os.getenv("LOG_SENSITIVE_DATA", "false").lower() == "true"

# Development Settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "false").lower() == "true"

def get_config_summary() -> Dict[str, Any]:
    """Get a summary of the current configuration."""
    return {
        "api": {
            "base_url": KANBAN_API_BASE_URL,
            "version": KANBAN_API_VERSION,
            "tenant_id": DEFAULT_TENANT_ID
        },
        "server": {
            "name": MCP_SERVER_NAME,
            "version": MCP_SERVER_VERSION,
            "debug_mode": DEBUG_MODE
        },
        "workflows": {
            "available_templates": list(WORKFLOW_TEMPLATES.keys()),
            "template_count": len(WORKFLOW_TEMPLATES)
        },
        "limits": {
            "max_title_length": MAX_TITLE_LENGTH,
            "max_description_length": MAX_DESCRIPTION_LENGTH,
            "max_card_description_length": MAX_CARD_DESCRIPTION_LENGTH,
            "priority_range": f"{MIN_PRIORITY}-{MAX_PRIORITY}",
            "default_limit": DEFAULT_LIMIT,
            "max_limit": MAX_LIMIT
        },
        "performance": {
            "request_timeout": REQUEST_TIMEOUT,
            "max_retries": MAX_RETRIES,
            "retry_delay": RETRY_DELAY
        }
    }
