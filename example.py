#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel到MySQL数据导入工具 - 示例脚本
展示如何在代码中使用该工具
"""

from excel_to_mysql import ExcelToMySQL

def example_import_users():
    """示例：导入用户数据"""
    print("=== 示例1：导入用户数据 ===")
    
    # 表结构定义
    table_structure = {
        'id': 'int',
        'name': 'varchar(50)',
        'age': 'int',
        'email': 'varchar(100)',
        'phone': 'varchar(20)',
        'address': 'text',
        'created_at': 'datetime'
    }
    
    # 创建导入器
    importer = ExcelToMySQL()
    
    # 执行导入
    success = importer.import_excel_to_mysql(
        table_name='users',
        table_structure=table_structure,
        excel_file_path='example_data/users.xlsx',
        sheet_name='Sheet1'
    )
    
    if success:
        print("✅ 用户数据导入成功!")
    else:
        print("❌ 用户数据导入失败!")

def example_import_products():
    """示例：导入产品数据"""
    print("\n=== 示例2：导入产品数据 ===")
    
    # 表结构定义
    table_structure = {
        'id': 'int',
        'name': 'varchar(100)',
        'description': 'text',
        'price': 'decimal(10,2)',
        'category': 'varchar(50)',
        'stock': 'int',
        'is_active': 'boolean'
    }
    
    # 创建导入器
    importer = ExcelToMySQL()
    
    # 执行导入
    success = importer.import_excel_to_mysql(
        table_name='products',
        table_structure=table_structure,
        excel_file_path='example_data/products.xlsx'
    )
    
    if success:
        print("✅ 产品数据导入成功!")
    else:
        print("❌ 产品数据导入失败!")

def example_import_orders():
    """示例：导入订单数据"""
    print("\n=== 示例3：导入订单数据 ===")
    
    # 表结构定义
    table_structure = {
        'id': 'int',
        'user_id': 'int',
        'product_id': 'int',
        'quantity': 'int',
        'amount': 'decimal(10,2)',
        'order_date': 'date',
        'status': 'varchar(20)'
    }
    
    # 创建导入器
    importer = ExcelToMySQL()
    
    # 执行导入
    success = importer.import_excel_to_mysql(
        table_name='orders',
        table_structure=table_structure,
        excel_file_path='example_data/orders.xlsx',
        sheet_name='Orders'
    )
    
    if success:
        print("✅ 订单数据导入成功!")
    else:
        print("❌ 订单数据导入失败!")

def create_sample_excel_files():
    """创建示例Excel文件（如果不存在）"""
    import pandas as pd
    import os
    
    # 创建示例数据目录
    os.makedirs('example_data', exist_ok=True)
    
    # 用户数据示例
    users_data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['张三', '李四', '王五', '赵六', '钱七'],
        'age': [25, 30, 35, 28, 32],
        'email': ['zhangsan@example.com', 'lisi@example.com', 'wangwu@example.com', 'zhaoliu@example.com', 'qianqi@example.com'],
        'phone': ['13800138001', '13800138002', '13800138003', '13800138004', '13800138005'],
        'address': ['北京市朝阳区', '上海市浦东新区', '广州市天河区', '深圳市南山区', '杭州市西湖区'],
        'created_at': ['2024-01-01 10:00:00', '2024-01-02 11:00:00', '2024-01-03 12:00:00', '2024-01-04 13:00:00', '2024-01-05 14:00:00']
    }
    
    # 产品数据示例
    products_data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['iPhone 15', 'MacBook Pro', 'iPad Air', 'Apple Watch', 'AirPods Pro'],
        'description': ['最新款iPhone', '专业级笔记本电脑', '轻薄平板电脑', '智能手表', '无线耳机'],
        'price': [5999.00, 12999.00, 3999.00, 2999.00, 1999.00],
        'category': ['手机', '电脑', '平板', '配件', '配件'],
        'stock': [100, 50, 80, 200, 150],
        'is_active': [True, True, True, True, True]
    }
    
    # 订单数据示例
    orders_data = {
        'id': [1, 2, 3, 4, 5],
        'user_id': [1, 2, 1, 3, 4],
        'product_id': [1, 2, 3, 4, 5],
        'quantity': [1, 1, 2, 1, 1],
        'amount': [5999.00, 12999.00, 7998.00, 2999.00, 1999.00],
        'order_date': ['2024-01-10', '2024-01-11', '2024-01-12', '2024-01-13', '2024-01-14'],
        'status': ['已完成', '处理中', '已完成', '已发货', '已完成']
    }
    
    # 创建DataFrame并保存为Excel
    users_df = pd.DataFrame(users_data)
    products_df = pd.DataFrame(products_data)
    orders_df = pd.DataFrame(orders_data)
    
    # 保存Excel文件
    users_df.to_excel('example_data/users.xlsx', index=False, sheet_name='Sheet1')
    products_df.to_excel('example_data/products.xlsx', index=False, sheet_name='Sheet1')
    orders_df.to_excel('example_data/orders.xlsx', index=False, sheet_name='Orders')
    
    print("✅ 示例Excel文件已创建在 example_data/ 目录下")

if __name__ == "__main__":
    print("Excel到MySQL数据导入工具 - 示例脚本")
    print("=" * 50)
    
    # 创建示例Excel文件
    create_sample_excel_files()
    
    # 运行示例
    try:
        example_import_users()
        example_import_products()
        example_import_orders()
    except Exception as e:
        print(f"运行示例时发生错误: {e}")
        print("请确保:")
        print("1. 数据库连接配置正确（在.env文件中）")
        print("2. MySQL服务正在运行")
        print("3. 数据库和用户已创建") 