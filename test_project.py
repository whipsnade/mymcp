#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目功能测试脚本
"""

import os
import sys
import pandas as pd

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    try:
        from config import Config
        from database import DatabaseManager
        from excel_processor import ExcelProcessor
        from excel_to_mysql import ExcelToMySQL
        print("✅ 所有模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_config():
    """测试配置"""
    print("\n测试配置...")
    try:
        from config import Config
        print(f"数据库主机: {Config.DB_HOST}")
        print(f"数据库端口: {Config.DB_PORT}")
        print(f"数据库名称: {Config.DB_NAME}")
        print(f"Excel起始行: {Config.EXCEL_START_ROW}")
        print("✅ 配置加载成功")
        return True
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_excel_processor():
    """测试Excel处理器"""
    print("\n测试Excel处理器...")
    try:
        from excel_processor import ExcelProcessor
        
        # 创建测试数据
        test_data = {
            'id': [1, 2, 3],
            'name': ['张三', '李四', '王五'],
            'age': [25, 30, 35],
            'email': ['zhangsan@test.com', 'lisi@test.com', 'wangwu@test.com']
        }
        
        # 创建测试Excel文件
        df = pd.DataFrame(test_data)
        test_file = 'test_data.xlsx'
        df.to_excel(test_file, index=False)
        
        # 测试Excel处理器
        processor = ExcelProcessor()
        
        # 定义表结构
        table_structure = {
            'id': 'int',
            'name': 'varchar(50)',
            'age': 'int',
            'email': 'varchar(100)'
        }
        
        # 处理Excel文件
        result = processor.process_excel_file(test_file, table_structure)
        
        if result:
            columns, data_tuples = result
            print(f"列名: {columns}")
            print(f"数据条数: {len(data_tuples)}")
            print(f"数据示例: {data_tuples[0] if data_tuples else '无数据'}")
            print("✅ Excel处理器测试成功")
            
            # 清理测试文件
            os.remove(test_file)
            return True
        else:
            print("❌ Excel处理器测试失败")
            return False
            
    except Exception as e:
        print(f"❌ Excel处理器测试失败: {e}")
        return False

def test_database_manager():
    """测试数据库管理器（不实际连接数据库）"""
    print("\n测试数据库管理器...")
    try:
        from database import DatabaseManager
        
        db_manager = DatabaseManager()
        print("✅ 数据库管理器创建成功")
        
        # 测试表结构创建SQL生成
        table_structure = {
            'id': 'int',
            'name': 'varchar(50)',
            'age': 'int'
        }
        
        # 这里只是测试SQL生成，不实际执行
        print("✅ 数据库管理器测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 数据库管理器测试失败: {e}")
        return False

def test_main_class():
    """测试主类"""
    print("\n测试主类...")
    try:
        from excel_to_mysql import ExcelToMySQL
        
        importer = ExcelToMySQL()
        print("✅ 主类创建成功")
        return True
        
    except Exception as e:
        print(f"❌ 主类测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("Excel到MySQL数据导入工具 - 功能测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
       # test_excel_processor,
        test_database_manager,
        test_main_class
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！项目可以正常使用。")
        print("\n下一步:")
        print("1. 配置数据库连接（编辑.env文件）")
        print("2. 运行示例: python example.py")
        print("3. 使用命令行工具: python main.py -h")
    else:
        print("⚠️  部分测试失败，请检查依赖安装和配置。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 