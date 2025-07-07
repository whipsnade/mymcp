#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Excel列名读取修复
"""

import pandas as pd
import tempfile
import os
from excel_processor import ExcelProcessor

def create_test_excel():
    """创建测试Excel文件，第一行是列名，第二行开始是数据"""
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

def test_column_reading():
    """测试列名读取是否正确"""
    print("=== 测试Excel列名读取修复 ===")
    
    # 创建测试Excel文件
    excel_file = create_test_excel()
    
    try:
        # 创建处理器
        processor = ExcelProcessor()
        
        # 读取Excel文件
        df = processor.read_excel(excel_file)
        
        if df is not None:
            print(f"✅ 成功读取Excel文件")
            print(f"列名: {list(df.columns)}")
            print(f"数据行数: {len(df)}")
            print(f"第一行数据: {df.iloc[0].tolist()}")
            
            # 验证列名是否正确
            expected_columns = ['name', 'age', 'email']
            if list(df.columns) == expected_columns:
                print("✅ 列名读取正确！")
            else:
                print(f"❌ 列名读取错误！期望: {expected_columns}, 实际: {list(df.columns)}")
        else:
            print("❌ 读取Excel文件失败")
            
    finally:
        # 清理临时文件
        os.unlink(excel_file)
    
    print("=== 测试完成 ===")

if __name__ == "__main__":
    test_column_reading() 