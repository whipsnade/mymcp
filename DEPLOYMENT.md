# Excel到MySQL MCP应用部署指南

## 概述

这是一个支持Dify框架的MCP（Model Context Protocol）应用，用于将Excel文件导入MySQL数据库。

## 功能特性

- ✅ 支持Excel文件URL下载
- ✅ 自动生成ID列（如果Excel中没有ID列）
- ✅ 自动处理空值和空字符
- ✅ 支持多种MySQL数据类型
- ✅ 批量插入提高性能
- ✅ 详细的日志记录
- ✅ 支持多工作表
- ✅ 自动获取数据库表结构

## 部署方式

### 方式一：本地部署

1. **克隆项目**
```bash
git clone <repository-url>
cd mysql-mcp
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置数据库**
```bash
cp env_example.txt .env
# 编辑 .env 文件，配置数据库连接信息
```

4. **启动MCP服务器**
```bash
python dify_mcp_server.py
```

### 方式二：Docker部署

1. **构建镜像**
```bash
docker build -t excel-to-mysql-mcp .
```

2. **运行容器**
```bash
docker run -d \
  --name excel-mysql-mcp \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env \
  excel-to-mysql-mcp
```

### 方式三：Docker Compose部署

1. **创建docker-compose.yml**
```yaml
version: '3.8'
services:
  excel-mysql-mcp:
    build: .
    container_name: excel-mysql-mcp
    volumes:
      - ./logs:/app/logs
      - ./.env:/app/.env
    environment:
      - PYTHONPATH=/app
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

2. **启动服务**
```bash
docker-compose up -d
```

## Dify集成配置

### 1. 在Dify中配置MCP应用

1. 登录Dify管理后台
2. 进入"应用" -> "工具" -> "自定义工具"
3. 点击"添加工具"
4. 选择"MCP协议"
5. 配置以下信息：

```
工具名称: Excel到MySQL导入工具
描述: 将Excel文件导入MySQL数据库
协议: MCP
服务器地址: http://your-server:8000
```

### 2. 工具配置

#### 工具1: import_excel_to_mysql
- **名称**: import_excel_to_mysql
- **描述**: 将Excel文件导入MySQL数据库
- **参数**:
  - `table_name` (string, 必需): 目标数据库表名
  - `excel_url` (string, 必需): Excel文件的URL地址
  - `sheet_name` (string, 可选): 工作表名称
  - `verbose` (boolean, 可选): 是否显示详细日志

#### 工具2: get_table_structure
- **名称**: get_table_structure
- **描述**: 获取MySQL数据库表的结构信息
- **参数**:
  - `table_name` (string, 必需): 要查询的表名

#### 工具3: test_database_connection
- **名称**: test_database_connection
- **描述**: 测试MySQL数据库连接
- **参数**: 无

### 3. 使用示例

#### 在Dify工作流中使用

1. **测试数据库连接**
```json
{
  "tool": "test_database_connection",
  "parameters": {}
}
```

2. **获取表结构**
```json
{
  "tool": "get_table_structure",
  "parameters": {
    "table_name": "users"
  }
}
```

3. **导入Excel文件**
```json
{
  "tool": "import_excel_to_mysql",
  "parameters": {
    "table_name": "users",
    "excel_url": "https://example.com/users.xlsx",
    "sheet_name": "Sheet1",
    "verbose": true
  }
}
```

## 环境变量配置

### 必需配置

```env
# 数据库配置
DB_HOST=your-database-host
DB_PORT=3306
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-database-name
DB_CHARSET=utf8mb4

# 日志配置
LOG_LEVEL=INFO
```

### 可选配置

```env
# Excel配置
EXCEL_START_ROW=2

# 服务器配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

## 监控和日志

### 日志文件

- `excel_to_mysql.log`: Excel导入操作日志
- `dify_mcp_server.log`: MCP服务器日志
- `mcp_server.log`: 简化版MCP服务器日志

### 监控指标

- 导入成功率
- 处理时间
- 错误率
- 数据库连接状态

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否运行
   - 验证连接参数是否正确
   - 确认网络连接

2. **Excel文件下载失败**
   - 检查URL是否可访问
   - 验证文件格式是否正确
   - 确认网络连接

3. **表结构不匹配**
   - 检查Excel列名与数据库表结构是否一致
   - 验证数据类型是否兼容
   - 查看详细错误日志

### 调试方法

1. **启用详细日志**
```bash
export LOG_LEVEL=DEBUG
python dify_mcp_server.py
```

2. **测试工具功能**
```bash
python test_mcp.py
```

3. **检查日志文件**
```bash
tail -f excel_to_mysql.log
tail -f dify_mcp_server.log
```

## 性能优化

### 数据库优化

1. **批量插入**
   - 使用`executemany`进行批量插入
   - 适当调整批量大小

2. **连接池**
   - 使用数据库连接池
   - 及时释放连接

3. **索引优化**
   - 为常用查询字段创建索引
   - 避免全表扫描

### 内存优化

1. **分块处理**
   - 大文件分块读取
   - 避免一次性加载全部数据

2. **垃圾回收**
   - 及时清理临时变量
   - 使用生成器处理大数据

## 安全考虑

1. **数据库安全**
   - 使用强密码
   - 限制数据库用户权限
   - 启用SSL连接

2. **文件安全**
   - 验证文件来源
   - 限制文件大小
   - 扫描恶意文件

3. **网络安全**
   - 使用HTTPS
   - 配置防火墙
   - 限制访问IP

## 更新和维护

### 版本更新

1. **备份数据**
```bash
mysqldump -u username -p database_name > backup.sql
```

2. **更新代码**
```bash
git pull origin main
pip install -r requirements.txt
```

3. **重启服务**
```bash
docker-compose restart
```

### 定期维护

1. **日志清理**
```bash
find /app/logs -name "*.log" -mtime +30 -delete
```

2. **数据库维护**
```sql
OPTIMIZE TABLE table_name;
ANALYZE TABLE table_name;
```

3. **系统监控**
   - 监控CPU和内存使用
   - 检查磁盘空间
   - 监控网络连接

## 联系支持

如有问题，请通过以下方式联系：

- GitHub Issues: [项目地址]
- 邮箱: your-email@example.com
- 文档: [文档地址] 