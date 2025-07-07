#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel到MySQL数据导入工具的MCP工具定义
支持Dify框架
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ImportExcelTool(BaseModel):
    """导入Excel到MySQL工具"""
    name: str = "import_excel_to_mysql"
    description: str = "将Excel文件导入MySQL数据库"
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "table_name": {
                "type": "string",
                "description": "目标数据库表名"
            },
            "excel_url": {
                "type": "string",
                "description": "Excel文件的URL地址"
            },
            "sheet_name": {
                "type": "string",
                "description": "工作表名称（可选）"
            },
            "verbose": {
                "type": "boolean",
                "description": "是否显示详细日志",
                "default": False
            }
        },
        "required": ["table_name", "excel_url"]
    }

class GetTableStructureTool(BaseModel):
    """获取表结构工具"""
    name: str = "get_table_structure"
    description: str = "获取MySQL数据库表的结构信息"
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "table_name": {
                "type": "string",
                "description": "要查询的表名"
            }
        },
        "required": ["table_name"]
    }

class TestDatabaseConnectionTool(BaseModel):
    """测试数据库连接工具"""
    name: str = "test_database_connection"
    description: str = "测试MySQL数据库连接"
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {},
        "required": []
    }

# 工具列表
TOOLS = [
    ImportExcelTool(),
    GetTableStructureTool(),
    TestDatabaseConnectionTool()
]

def get_tools_schema() -> List[Dict[str, Any]]:
    """获取工具模式定义"""
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters
        }
        for tool in TOOLS
    ]

def get_tool_by_name(name: str) -> Optional[BaseModel]:
    """根据名称获取工具"""
    for tool in TOOLS:
        if tool.name == name:
            return tool
    return None 