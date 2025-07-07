#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dify兼容的MCP服务器实现
Excel到MySQL数据导入工具
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from excel_to_mysql import ExcelToMySQL
from config import Config
from tools import get_tools_schema, get_tool_by_name

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('dify_mcp_server.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class DifyMCPServer:
    """Dify兼容的MCP服务器"""
    
    def __init__(self):
        self.importer = ExcelToMySQL()
        self.tools_schema = get_tools_schema()
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理Dify请求"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            
            if method == "tools/list":
                return await self.list_tools()
            elif method == "tools/call":
                return await self.call_tool(params)
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        except Exception as e:
            logger.error(f"处理请求时发生错误: {e}")
            return {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    async def list_tools(self) -> Dict[str, Any]:
        """列出可用工具"""
        return {
            "result": {
                "tools": self.tools_schema
            }
        }
    
    async def call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """调用工具"""
        tool_name = params.get("name")
        tool_params = params.get("arguments", {})
        
        if tool_name == "import_excel_to_mysql":
            return await self.import_excel_to_mysql(tool_params)
        elif tool_name == "get_table_structure":
            return await self.get_table_structure(tool_params)
        elif tool_name == "test_database_connection":
            return await self.test_database_connection(tool_params)
        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Tool not found: {tool_name}"
                }
            }
    
    async def import_excel_to_mysql(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """导入Excel到MySQL"""
        try:
            table_name = params.get("table_name")
            excel_url = params.get("excel_url")
            sheet_name = params.get("sheet_name")
            verbose = params.get("verbose", False)
            
            if not table_name or not excel_url:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameters: table_name and excel_url"
                    }
                }
            
            logger.info(f"开始导入Excel文件: {excel_url}")
            logger.info(f"目标表名: {table_name}")
            
            # 执行导入
            success = self.importer.import_excel_to_mysql(
                table_name=table_name,
                excel_file_path=excel_url,
                sheet_name=sheet_name
            )
            
            if success:
                # 获取导入的记录数
                imported_count = 0
                try:
                    with open('excel_to_mysql.log', 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line in reversed(lines):
                            if '成功导入' in line and '条记录' in line:
                                import re
                                match = re.search(r'成功导入(\d+)条记录', line)
                                if match:
                                    imported_count = int(match.group(1))
                                break
                except:
                    pass
                
                return {
                    "result": {
                        "success": True,
                        "message": f"成功导入Excel文件到表 '{table_name}'",
                        "imported_count": imported_count,
                        "table_name": table_name
                    }
                }
            else:
                return {
                    "result": {
                        "success": False,
                        "message": "导入失败，请检查日志文件获取详细信息"
                    }
                }
                
        except Exception as e:
            logger.error(f"导入过程中发生错误: {e}")
            return {
                "result": {
                    "success": False,
                    "message": f"导入失败: {str(e)}"
                }
            }
    
    async def get_table_structure(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """获取表结构"""
        try:
            table_name = params.get("table_name")
            
            if not table_name:
                return {
                    "error": {
                        "code": -32602,
                        "message": "Missing required parameter: table_name"
                    }
                }
            
            if not self.importer.db_manager.connect():
                return {
                    "result": {
                        "success": False,
                        "message": "数据库连接失败"
                    }
                }
            
            table_structure = self.importer.db_manager.get_table_structure(table_name)
            self.importer.db_manager.disconnect()
            
            if table_structure:
                return {
                    "result": {
                        "success": True,
                        "message": f"成功获取表 '{table_name}' 的结构",
                        "table_name": table_name,
                        "structure": table_structure,
                        "column_count": len(table_structure)
                    }
                }
            else:
                return {
                    "result": {
                        "success": False,
                        "message": f"表 '{table_name}' 不存在或无法获取结构"
                    }
                }
                
        except Exception as e:
            logger.error(f"获取表结构失败: {e}")
            return {
                "result": {
                    "success": False,
                    "message": f"获取表结构失败: {str(e)}"
                }
            }
    
    async def test_database_connection(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """测试数据库连接"""
        try:
            if self.importer.db_manager.connect():
                self.importer.db_manager.disconnect()
                return {
                    "result": {
                        "success": True,
                        "message": "数据库连接测试成功",
                        "host": Config.DB_HOST,
                        "port": Config.DB_PORT,
                        "database": Config.DB_NAME
                    }
                }
            else:
                return {
                    "result": {
                        "success": False,
                        "message": "数据库连接测试失败"
                    }
                }
                
        except Exception as e:
            logger.error(f"数据库连接测试失败: {e}")
            return {
                "result": {
                    "success": False,
                    "message": f"数据库连接测试失败: {str(e)}"
                }
            }

async def main():
    """主函数"""
    server = DifyMCPServer()
    
    # 从标准输入读取请求
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            # 输出响应到标准输出
            print(json.dumps(response, ensure_ascii=False))
            sys.stdout.flush()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"处理请求时发生错误: {e}")
            error_response = {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response, ensure_ascii=False))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main()) 