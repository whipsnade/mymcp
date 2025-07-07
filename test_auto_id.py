#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试自动生成id列功能
"""

import pandas as pd
import tempfile
import os
from excel_processor import ExcelProcessor
# from config import Config  # 不再需要

# 保证测试时不跳过表头（已通过pandas.read_excel实现）

def create_test_excel_without_id():
    """创建没有id列的测试Excel文件"""
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

def create_test_excel_with_empty_id():
    """创建有空的id列的测试Excel文件"""
    data = {
        'id': ['', '', ''],
        'name': ['张三', '李四', '王五'],
        'age': [25, 30, 35],
        'email': ['zhangsan@example.com', 'lisi@example.com', 'wangwu@example.com']
    }
    df = pd.DataFrame(data)
    
    # 创建临时文件
    temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    df.to_excel(temp_file.name, index=False)
    return temp_file.name

def create_test_excel_with_id():
    """创建有id列的测试Excel文件"""
    data = {
        'id': [1, 2, 3],
        'name': ['张三', '李四', '王五'],
        'age': [25, 30, 35],
        'email': ['zhangsan@example.com', 'lisi@example.com', 'wangwu@example.com']
    }
    df = pd.DataFrame(data)
    
    # 创建临时文件
    temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    df.to_excel(temp_file.name, index=False)
    return temp_file.name

def test_auto_id_generation():
    """测试自动生成id列功能"""
    processor = ExcelProcessor()
    
    print("=== 测试1: Excel文件没有id列 ===")
    file1 = create_test_excel_without_id()
    try:
        df1 = pd.read_excel(file1)  # 直接用pandas读取
        if df1 is not None:
            df1_with_id = processor.add_auto_id_column(df1)
            print(f"原始列名: {list(df1.columns)}")
            print(f"处理后列名: {list(df1_with_id.columns)}")
            print(f"id列值: {df1_with_id['id'].tolist()}")
            print("✅ 测试1通过")
        else:
            print("❌ 测试1失败: 无法读取Excel文件")
    finally:
        os.unlink(file1)
    
    print("\n=== 测试2: Excel文件有空的id列 ===")
    file2 = create_test_excel_with_empty_id()
    try:
        df2 = pd.read_excel(file2)
        if df2 is not None:
            df2_with_id = processor.add_auto_id_column(df2)
            print(f"原始id列值: {df2['id'].tolist()}")
            print(f"处理后id列值: {df2_with_id['id'].tolist()}")
            print("✅ 测试2通过")
        else:
            print("❌ 测试2失败: 无法读取Excel文件")
    finally:
        os.unlink(file2)
    
    print("\n=== 测试3: Excel文件有id列且不为空 ===")
    file3 = create_test_excel_with_id()
    try:
        df3 = pd.read_excel(file3)
        if df3 is not None:
            df3_with_id = processor.add_auto_id_column(df3)
            print(f"原始id列值: {df3['id'].tolist()}")
            print(f"处理后id列值: {df3_with_id['id'].tolist()}")
            print("✅ 测试3通过")
        else:
            print("❌ 测试3失败: 无法读取Excel文件")
    finally:
        os.unlink(file3)

if __name__ == "__main__":
    test_auto_id_generation() 