#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试列名匹配问题调试
"""

import pandas as pd
import tempfile
import os
from excel_processor import ExcelProcessor

def create_test_excel_with_chinese_columns():
    """创建包含中文字符列名的测试Excel文件"""
    data = {
        '合同分类': ['A类', 'B类', 'C类'],
        '合同金额': [1000, 2000, 3000],
        '签订日期': ['2024-01-01', '2024-01-02', '2024-01-03']
    }
    df = pd.DataFrame(data)
    
    # 创建临时文件
    temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    df.to_excel(temp_file.name, index=False)
    return temp_file.name

def test_column_debug():
    """测试列名匹配问题"""
    print("=== 测试列名匹配问题调试 ===")
    
    # 创建测试Excel文件
    excel_file = create_test_excel_with_chinese_columns()
    
    try:
        # 创建处理器
        processor = ExcelProcessor()
        
        # 模拟数据库表结构（与Excel列名不匹配）
        table_structure = {
            '合同分类': 'varchar(50)',
            '合同金额': 'decimal(10,2)',
            '签订日期': 'date',
            '不存在的列': 'varchar(100)'  # 添加一个不存在的列
        }
        
        print(f"测试Excel文件路径: {excel_file}")
        print("数据库表结构:", table_structure)
        print("\n开始处理Excel文件...")
        print("注意：这个测试会失败，但会显示详细的错误信息")
        
        # 处理Excel文件
        result = processor.process_excel_file(excel_file, table_structure)
        
        if result is not None:
            columns, data_tuples = result
            print(f"\n✅ 处理成功！")
            print(f"最终列名: {columns}")
            print(f"数据条数: {len(data_tuples)}")
        else:
            print("\n❌ 处理失败！")
            print("请查看日志文件获取详细的错误信息")
            
    finally:
        # 清理临时文件
        os.unlink(excel_file)
    
    print("\n=== 测试完成 ===")
    print("请查看日志文件 'excel_to_mysql.log' 获取详细的调试信息")

if __name__ == "__main__":
    test_column_debug() 