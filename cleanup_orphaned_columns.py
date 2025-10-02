#!/usr/bin/env python3
"""
Orphaned Column Cleanup Script
Safely deletes only orphaned columns that reference non-existent boards
"""

import requests
import json
from typing import List, Set

# API Configuration
BASE_URL = "http://localhost:8000/v1"
HEADERS = {"Content-Type": "application/json"}

def get_all_boards() -> Set[str]:
    """Get all valid board IDs"""
    print("🔍 Fetching all valid boards...")
    valid_board_ids = set()
    
    offset = 0
    limit = 100
    
    while True:
        url = f"{BASE_URL}/boards/?limit={limit}&offset={offset}"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"❌ Error fetching boards: {response.status_code}")
            break
            
        data = response.json()
        boards = data.get("data", [])
        
        if not boards:
            break
            
        for board in boards:
            valid_board_ids.add(board["id"])
        
        # Check if there are more pages
        pagination = data.get("pagination", {})
        if not pagination.get("has_next", False):
            break
            
        offset += limit
    
    print(f"✅ Found {len(valid_board_ids)} valid boards")
    return valid_board_ids

def get_all_columns() -> List[dict]:
    """Get all columns"""
    print("🔍 Fetching all columns...")
    all_columns = []
    
    offset = 0
    limit = 100
    
    while True:
        url = f"{BASE_URL}/columns/?limit={limit}&offset={offset}"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"❌ Error fetching columns: {response.status_code}")
            break
            
        data = response.json()
        columns = data.get("data", [])
        
        if not columns:
            break
            
        all_columns.extend(columns)
        
        # Check if there are more pages
        pagination = data.get("pagination", {})
        if not pagination.get("has_next", False):
            break
            
        offset += limit
    
    print(f"✅ Found {len(all_columns)} total columns")
    return all_columns

def delete_orphaned_columns(valid_board_ids: Set[str], all_columns: List[dict]):
    """Delete only orphaned columns"""
    print("🔍 Identifying orphaned columns...")
    
    orphaned_columns = []
    valid_columns = []
    
    for column in all_columns:
        board_id = column.get("board_id")
        if board_id not in valid_board_ids:
            orphaned_columns.append(column)
        else:
            valid_columns.append(column)
    
    print(f"✅ Found {len(valid_columns)} valid columns")
    print(f"🚨 Found {len(orphaned_columns)} orphaned columns")
    
    if not orphaned_columns:
        print("🎉 No orphaned columns to delete!")
        return
    
    print(f"\n🗑️  Starting deletion of {len(orphaned_columns)} orphaned columns...")
    
    deleted_count = 0
    failed_count = 0
    
    for i, column in enumerate(orphaned_columns, 1):
        column_id = column["id"]
        column_name = column.get("name", "Unknown")
        board_id = column["board_id"]
        
        print(f"[{i}/{len(orphaned_columns)}] Deleting column '{column_name}' (ID: {column_id}) - references non-existent board {board_id}")
        
        url = f"{BASE_URL}/columns/{column_id}"
        response = requests.delete(url, headers=HEADERS)
        
        if response.status_code == 200:
            print(f"   ✅ Successfully deleted")
            deleted_count += 1
        else:
            print(f"   ❌ Failed to delete: {response.status_code}")
            failed_count += 1
    
    print(f"\n🎉 CLEANUP COMPLETE!")
    print(f"✅ Successfully deleted: {deleted_count} orphaned columns")
    print(f"❌ Failed to delete: {failed_count} orphaned columns")

def main():
    """Main cleanup function"""
    print("🧹 ORPHANED COLUMN CLEANUP SCRIPT")
    print("=" * 50)
    
    try:
        # Step 1: Get all valid board IDs
        valid_board_ids = get_all_boards()
        
        # Step 2: Get all columns
        all_columns = get_all_columns()
        
        # Step 3: Delete orphaned columns
        delete_orphaned_columns(valid_board_ids, all_columns)
        
    except Exception as e:
        print(f"❌ Script failed with error: {e}")

if __name__ == "__main__":
    main()






