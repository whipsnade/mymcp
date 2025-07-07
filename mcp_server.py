#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel到MySQL数据导入工具的MCP服务器
支持Dify框架的MCP应用
"""

import asyncio
import json
import logging
import tempfile
import os
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from excel_to_mysql import ExcelToMySQL
from config import Config

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('mcp_server.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class ImportExcelRequest(BaseModel):
    """导入Excel请求模型"""
    table_name: str = Field(..., description="目标数据库表名")
    excel_url: str = Field(..., description="Excel文件的URL地址")
    sheet_name: Optional[str] = Field(None, description="工作表名称（可选）")
    verbose: bool = Field(False, description="是否显示详细日志")

class ImportExcelResponse(BaseModel):
    """导入Excel响应模型"""
    success: bool = Field(..., description="导入是否成功")
    message: str = Field(..., description="响应消息")
    imported_count: Optional[int] = Field(None, description="导入的记录数")
    table_name: Optional[str] = Field(None, description="表名")
    columns: Optional[List[str]] = Field(None, description="导入的列名")

class MCPExcelToMySQLServer:
    """MCP Excel到MySQL导入服务器"""
    
    def __init__(self):
        self.importer = ExcelToMySQL()
    
    async def import_excel_to_mysql(self, request: ImportExcelRequest) -> ImportExcelResponse:
        """
        将Excel文件导入MySQL数据库
        
        Args:
            request: 导入请求参数
            
        Returns:
            ImportExcelResponse: 导入结果
        """
        try:
            logger.info(f"开始导入Excel文件: {request.excel_url}")
            logger.info(f"目标表名: {request.table_name}")
            
            # 执行导入
            success = self.importer.import_excel_to_mysql(
                table_name=request.table_name,
                excel_file_path=request.excel_url,
                sheet_name=request.sheet_name
            )
            
            if success:
                # 获取导入的记录数（这里简化处理，实际可以从日志中解析）
                imported_count = 0
                try:
                    with open('excel_to_mysql.log', 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line in reversed(lines):
                            if '成功导入' in line and '条记录' in line:
                                # 解析记录数
                                import re
                                match = re.search(r'成功导入(\d+)条记录', line)
                                if match:
                                    imported_count = int(match.group(1))
                                break
                except:
                    pass
                
                return ImportExcelResponse(
                    success=True,
                    message=f"成功导入Excel文件到表 '{request.table_name}'",
                    imported_count=imported_count,
                    table_name=request.table_name,
                    columns=None
                )
            else:
                return ImportExcelResponse(
                    success=False,
                    message="导入失败，请检查日志文件获取详细信息",
                    imported_count=None,
                    table_name=None,
                    columns=None
                )
                
        except Exception as e:
            logger.error(f"导入过程中发生错误: {e}")
            return ImportExcelResponse(
                success=False,
                message=f"导入失败: {str(e)}",
                imported_count=None,
                table_name=None,
                columns=None
            )
    
    async def get_table_structure(self, table_name: str) -> Dict[str, Any]:
        """
        获取数据库表结构
        
        Args:
            table_name: 表名
            
        Returns:
            Dict: 表结构信息
        """
        try:
            if not self.importer.db_manager.connect():
                return {
                    "success": False,
                    "message": "数据库连接失败"
                }
            
            table_structure = self.importer.db_manager.get_table_structure(table_name)
            self.importer.db_manager.disconnect()
            
            if table_structure:
                return {
                    "success": True,
                    "message": f"成功获取表 '{table_name}' 的结构",
                    "table_name": table_name,
                    "structure": table_structure,
                    "column_count": len(table_structure)
                }
            else:
                return {
                    "success": False,
                    "message": f"表 '{table_name}' 不存在或无法获取结构"
                }
                
        except Exception as e:
            logger.error(f"获取表结构失败: {e}")
            return {
                "success": False,
                "message": f"获取表结构失败: {str(e)}"
            }
    
    async def test_database_connection(self) -> Dict[str, Any]:
        """
        测试数据库连接
        
        Returns:
            Dict: 连接测试结果
        """
        try:
            if self.importer.db_manager.connect():
                self.importer.db_manager.disconnect()
                return {
                    "success": True,
                    "message": "数据库连接测试成功",
                    "host": Config.DB_HOST,
                    "port": Config.DB_PORT,
                    "database": Config.DB_NAME
                }
            else:
                return {
                    "success": False,
                    "message": "数据库连接测试失败"
                }
                
        except Exception as e:
            logger.error(f"数据库连接测试失败: {e}")
            return {
                "success": False,
                "message": f"数据库连接测试失败: {str(e)}"
            }

async def main():
    """主函数"""
    # 创建MCP服务器
    mcp_server = MCPExcelToMySQLServer()
    
    # 简单的测试
    print("MCP Excel到MySQL服务器已启动")
    print("可用功能:")
    print("1. import_excel_to_mysql - 导入Excel到MySQL")
    print("2. get_table_structure - 获取表结构")
    print("3. test_database_connection - 测试数据库连接")

if __name__ == "__main__":
    asyncio.run(main()) 