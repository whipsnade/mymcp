# Excel到MySQL数据导入工具

一个功能强大的Python工具，用于将Excel文件中的数据导入MySQL数据库。支持从Excel第二行开始读取数据，自动处理空字符和空值。**现已支持Dify框架的MCP应用！**

## 功能特性

- ✅ 从Excel文件第二行开始读取数据
- ✅ 自动处理空字符和空值（转换为NULL）
- ✅ 支持多种MySQL数据类型
- ✅ 批量插入，提高性能
- ✅ 详细的日志记录
- ✅ 命令行和编程接口
- ✅ 自动创建表结构
- ✅ 支持多工作表
- ✅ **自动生成ID列（如果Excel中没有ID列）**
- ✅ **支持Dify框架的MCP应用**

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置数据库

1. 复制环境变量示例文件：
```bash
cp env_example.txt .env
```

2. 编辑 `.env` 文件，配置数据库连接信息：
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=test
DB_CHARSET=utf8mb4
LOG_LEVEL=INFO
```

## 使用方法

### 命令行使用

基本语法：
```bash
python main.py -t 表名 -f Excel文件URL
```

#### 示例1：导入用户数据
```bash
python main.py -t users -f https://example.com/users.xlsx
```

#### 示例2：导入产品数据到指定工作表
```bash
python main.py -t products -f https://example.com/products.xlsx -w "Sheet1"
```

#### 示例3：显示详细日志
```bash
python main.py -t orders -f https://example.com/orders.xlsx -v
```

### 编程接口使用

```python
from excel_to_mysql import ExcelToMySQL

# 创建导入器
importer = ExcelToMySQL()

# 执行导入（会自动从数据库获取表结构）
success = importer.import_excel_to_mysql(
    table_name='users',
    excel_file_path='https://example.com/users.xlsx',
    sheet_name='Sheet1'  # 可选
)

if success:
    print("导入成功!")
else:
    print("导入失败!")
```

### MCP应用使用（Dify框架）

#### 启动MCP服务器

```bash
python dify_mcp_server.py
```

#### 可用工具

1. **import_excel_to_mysql** - 导入Excel到MySQL
   - `table_name`: 目标数据库表名
   - `excel_url`: Excel文件的URL地址
   - `sheet_name`: 工作表名称（可选）
   - `verbose`: 是否显示详细日志

2. **get_table_structure** - 获取表结构
   - `table_name`: 要查询的表名

3. **test_database_connection** - 测试数据库连接

#### 测试MCP功能

```bash
python test_mcp.py
```

## 支持的MySQL数据类型

- **整数类型**: `int`, `bigint`, `smallint`, `tinyint`
- **字符串类型**: `varchar(n)`, `char(n)`, `text`, `longtext`
- **小数类型**: `decimal(m,d)`, `float`, `double`
- **日期时间类型**: `date`, `datetime`, `timestamp`
- **布尔类型**: `boolean`, `bool`
- **其他类型**: `json`, `blob`

## Excel文件格式要求

1. **第一行必须是列名**：与表结构中的列名对应
2. **数据从第二行开始**：工具会自动跳过第一行
3. **支持的文件格式**：`.xlsx`, `.xls`
4. **空值处理**：空字符、空格字符串、NaN值都会被转换为NULL
5. **自动ID生成**：如果Excel没有ID列，会自动生成自增长的ID列

## 示例Excel文件格式

| id | name | age | email |
|----|------|-----|-------|
| 1  | 张三 | 25  | zhangsan@example.com |
| 2  | 李四 | 30  | lisi@example.com |
| 3  | 王五 | 35  | wangwu@example.com |

## 运行示例

```bash
# 运行示例脚本（会创建示例Excel文件并演示导入）
python example.py

# 测试MCP功能
python test_mcp.py
```

## 项目结构

```
mysql-mcp/
├── main.py                    # 命令行入口
├── example.py                 # 示例脚本
├── excel_to_mysql.py          # 主要导入类
├── database.py                # 数据库操作类
├── excel_processor.py         # Excel处理类
├── config.py                  # 配置管理
├── requirements.txt           # 依赖包
├── env_example.txt           # 环境变量示例
├── README.md                 # 项目说明
├── dify_mcp_server.py        # Dify MCP服务器
├── tools.py                  # MCP工具定义
├── schema.json               # MCP应用描述
├── mcp_server.py             # MCP服务器（简化版）
├── test_mcp.py               # MCP功能测试
└── example_data/             # 示例数据目录
    ├── users.xlsx
    ├── products.xlsx
    └── orders.xlsx
```

## MCP应用特性

### 支持Dify框架
- 完整的MCP协议实现
- 标准化的工具定义
- JSON-RPC通信协议
- 异步处理支持

### 工具功能
1. **Excel导入工具**：支持URL下载、自动ID生成、批量插入
2. **表结构查询工具**：获取数据库表结构信息
3. **连接测试工具**：验证数据库连接配置

### 错误处理
- 完善的错误码定义
- 详细的错误信息
- 日志记录和调试支持

## 错误处理

工具包含完善的错误处理机制：

- 数据库连接失败
- Excel文件不存在或格式错误
- 表结构与Excel列不匹配
- 数据类型转换错误
- 空值处理
- MCP协议错误

所有错误都会记录到日志文件中（`excel_to_mysql.log` 和 `dify_mcp_server.log`）。

## 性能优化

- 使用批量插入（`executemany`）提高性能
- 自动处理空值，减少数据传输
- 支持大量数据导入
- 异步处理支持

## 注意事项

1. 确保MySQL服务正在运行
2. 确保数据库和用户已创建
3. 确保用户有创建表和插入数据的权限
4. Excel文件第一行必须是列名
5. 表结构中的列名必须与Excel列名完全匹配
6. 支持http/https的Excel文件URL
7. MCP应用需要Python 3.8+

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！ 