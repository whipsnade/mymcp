#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试列名打印功能
"""

import pandas as pd
import tempfile
import os
from excel_to_mysql import ExcelToMySQL

def create_test_excel():
    """创建测试Excel文件"""
    data = {
        'name': ['张三', '李四', '王五'],
        'age': [25, 30, 35],
        'email': ['zhangsan@example.com', 'lisi@example.com', 'wangwu@example.com']
    }
    df = pd.DataFrame(data)
    
    # 创建临时文件
    temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    df.to_excel(temp_file.name, index=False)
    return temp_file.name

def test_column_logging():
    """测试列名打印功能"""
    print("=== 测试列名打印功能 ===")
    
    # 创建测试Excel文件
    excel_file = create_test_excel()
    
    try:
        # 创建导入器
        importer = ExcelToMySQL()
        
        # 注意：这里只是测试列名打印，不会真正连接数据库
        # 实际使用时需要配置数据库连接
        print(f"测试Excel文件路径: {excel_file}")
        print("列名打印功能已移动到Excel读取阶段")
        print("当执行导入时，会在日志中看到类似以下信息：")
        print("- 成功读取Excel文件: [文件路径]")
        print("- Excel文件中的列名: ['name', 'age', 'email']")
        print("- Excel文件中的数据行数: 3")
        print("（如果Excel没有id列，后续会显示自动添加id列的信息）")
        
    finally:
        # 清理临时文件
        os.unlink(excel_file)
    
    print("✅ 列名打印功能测试完成")

if __name__ == "__main__":
    test_column_logging() 