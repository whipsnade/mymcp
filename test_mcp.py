#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试MCP功能
"""

import asyncio
import json
from dify_mcp_server import DifyMCPServer

async def test_mcp_server():
    """测试MCP服务器功能"""
    print("=== 测试MCP服务器功能 ===")
    
    server = DifyMCPServer()
    
    # 测试1: 列出工具
    print("\n1. 测试列出工具")
    request = {
        "method": "tools/list",
        "params": {}
    }
    response = await server.handle_request(request)
    print(f"响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
    
    # 测试2: 测试数据库连接
    print("\n2. 测试数据库连接")
    request = {
        "method": "tools/call",
        "params": {
            "name": "test_database_connection",
            "arguments": {}
        }
    }
    response = await server.handle_request(request)
    print(f"响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
    
    # 测试3: 获取表结构
    print("\n3. 测试获取表结构")
    request = {
        "method": "tools/call",
        "params": {
            "name": "get_table_structure",
            "arguments": {
                "table_name": "users"
            }
        }
    }
    response = await server.handle_request(request)
    print(f"响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
    
    # 测试4: 导入Excel（模拟）
    print("\n4. 测试导入Excel（模拟）")
    request = {
        "method": "tools/call",
        "params": {
            "name": "import_excel_to_mysql",
            "arguments": {
                "table_name": "test_table",
                "excel_url": "https://example.com/test.xlsx",
                "sheet_name": "Sheet1",
                "verbose": True
            }
        }
    }
    response = await server.handle_request(request)
    print(f"响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 