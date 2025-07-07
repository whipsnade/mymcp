#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel到MySQL数据导入工具
支持从Excel文件第二行开始读取数据并导入MySQL数据库
"""

import argparse
import sys
import tempfile
import os
import shutil
from typing import Dict
from urllib.parse import urlparse
from urllib.request import urlopen
from excel_to_mysql import ExcelToMySQL

def download_excel_file(url: str) -> str:
    """
    下载Excel文件到临时目录，返回本地文件路径
    """
    try:
        with urlopen(url) as response:
            if response.status != 200:
                print(f"下载失败，HTTP状态码: {response.status}")
                return ''
            suffix = '.xlsx' if url.lower().endswith('.xlsx') else '.xls'
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                shutil.copyfileobj(response, tmp_file)
                return tmp_file.name
    except Exception as e:
        print(f"下载Excel文件失败: {e}")
        return ''

def get_table_structure_from_db(table_name: str) -> Dict[str, str]:
    """
    通过表名从数据库获取表结构
    """
    try:
        from database import DatabaseManager
        
        db_manager = DatabaseManager()
        if not db_manager.connect():
            print("数据库连接失败")
            return {}
        
        # 获取表结构
        structure = db_manager.get_table_structure(table_name)
        db_manager.disconnect()
        
        if not structure:
            print(f"表 '{table_name}' 不存在或无法获取结构")
            return {}
        
        return structure
        
    except Exception as e:
        print(f"获取表结构失败: {e}")
        return {}

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='将Excel数据导入MySQL数据库',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py -t users -f https://example.com/users.xlsx
  python main.py -t products -f https://example.com/products.xlsx -w "Sheet1"
        """
    )
    
    parser.add_argument('-t', '--table', required=True, help='表名')
    parser.add_argument('-f', '--file', required=True, help='Excel文件URL')
    parser.add_argument('-w', '--worksheet', help='工作表名称（可选）')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细日志')
    
    args = parser.parse_args()
    
    # 验证URL格式
    file_url = args.file
    if not (file_url.startswith('http://') or file_url.startswith('https://')):
        print("错误: 文件参数必须是有效的URL")
        sys.exit(1)
    
    # 下载Excel文件
    print(f"开始下载Excel文件: {file_url}")
    local_file_path = download_excel_file(file_url)
    if not local_file_path:
        print("下载Excel文件失败，无法继续")
        sys.exit(1)
    print(f"Excel文件已下载到: {local_file_path}")
    
    # 通过表名获取数据库结构
    print(f"获取表 '{args.table}' 的结构...")
    table_structure = get_table_structure_from_db(args.table)
    if not table_structure:
        print(f"无法获取表 '{args.table}' 的结构，请确保表已存在")
        # 清理临时文件
        if os.path.exists(local_file_path):
            os.remove(local_file_path)
        sys.exit(1)
    
    print(f"表结构: {table_structure}")
    
    # 创建导入器
    importer = ExcelToMySQL()
    
    # 执行导入
    print(f"开始导入数据到表 '{args.table}'...")
    print(f"Excel文件: {local_file_path}")
    if args.worksheet:
        print(f"工作表: {args.worksheet}")
    
    success = importer.import_excel_to_mysql(
        table_name=args.table,
        table_structure=table_structure,
        excel_file_path=local_file_path,
        sheet_name=args.worksheet
    )
    
    # 清理临时文件
    if os.path.exists(local_file_path):
        os.remove(local_file_path)
        print(f"已删除临时文件: {local_file_path}")
    
    if success:
        print("✅ 数据导入成功!")
    else:
        print("❌ 数据导入失败!")
        sys.exit(1)

def example_usage():
    """示例用法"""
    print("""
=== Excel到MySQL数据导入工具 ===

基本用法:
python main.py -t 表名 -f Excel文件URL

参数说明:
-t, --table      表名（必须已存在于数据库中）
-f, --file       Excel文件URL
-w, --worksheet  工作表名称（可选）
-v, --verbose    显示详细日志

示例:
1. 导入用户数据:
   python main.py -t users -f https://example.com/users.xlsx

2. 导入产品数据到指定工作表:
   python main.py -t products -f https://example.com/products.xlsx -w "Sheet1"

3. 显示详细日志:
   python main.py -t orders -f https://example.com/orders.xlsx -v

注意事项:
1. Excel文件第一行必须是列名
2. 数据从第二行开始读取
3. 空字符和空值会被自动处理为NULL
4. 确保数据库连接配置正确（在.env文件中）
5. 表必须已存在于数据库中
6. Excel列名必须与数据库表字段名完全匹配
7. 支持http/https的Excel文件URL
    """)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        example_usage()
    else:
        main() 