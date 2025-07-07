import pymysql
import logging
from typing import List, Dict, Any
from config import Config

class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self):
        self.connection = None
        self.logger = logging.getLogger(__name__)
    
    def connect(self) -> bool:
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                charset=Config.DB_CHARSET,
                autocommit=True
            )
            self.logger.info("数据库连接成功")
            return True
        except Exception as e:
            self.logger.error(f"数据库连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            self.logger.info("数据库连接已断开")
    
    def execute_sql(self, sql: str, params: tuple | None = None) -> bool:
        """执行SQL语句"""
        if not self.connection:
            self.logger.error("数据库未连接")
            return False
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                self.logger.info(f"SQL执行成功: {sql[:100]}...")
                return True
        except Exception as e:
            self.logger.error(f"SQL执行失败: {e}")
            return False
    
    def execute_many(self, sql: str, params_list: List[tuple]) -> bool:
        """批量执行SQL语句"""
        if not self.connection:
            self.logger.error("数据库未连接")
            return False
        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(sql, params_list)
                self.logger.info(f"批量SQL执行成功，共{len(params_list)}条记录")
                return True
        except Exception as e:
            self.logger.error(f"批量SQL执行失败: {e}")
            return False
    
    def create_table(self, table_name: str, table_structure: Dict[str, str]) -> bool:
        """创建表"""
        columns = []
        for column_name, column_type in table_structure.items():
            columns.append(f"`{column_name}` {column_type}")
        
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            {', '.join(columns)}
        ) ENGINE=InnoDB DEFAULT CHARSET={Config.DB_CHARSET}
        """
        
        return self.execute_sql(create_sql)
    
    def insert_data(self, table_name: str, columns: List[str], data_list: List[tuple]) -> bool:
        """插入数据"""
        if not data_list:
            self.logger.warning("没有数据需要插入")
            return True
        
        # 构建INSERT语句
        columns_str = ', '.join([f"`{col}`" for col in columns])
        placeholders = ', '.join(['%s'] * len(columns))
        insert_sql = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
        
        return self.execute_many(insert_sql, data_list)
    
    def get_table_structure(self, table_name: str) -> Dict[str, str]:
        """获取表结构"""
        if not self.connection:
            self.logger.error("数据库未连接")
            return {}
        
        try:
            with self.connection.cursor() as cursor:
                # 获取表结构信息
                cursor.execute(f"""
                    SELECT COLUMN_NAME, DATA_TYPE, 
                           CASE 
                               WHEN CHARACTER_MAXIMUM_LENGTH IS NOT NULL 
                               THEN CONCAT(DATA_TYPE, '(', CHARACTER_MAXIMUM_LENGTH, ')')
                               WHEN NUMERIC_PRECISION IS NOT NULL AND NUMERIC_SCALE IS NOT NULL
                               THEN CONCAT(DATA_TYPE, '(', NUMERIC_PRECISION, ',', NUMERIC_SCALE, ')')
                               WHEN NUMERIC_PRECISION IS NOT NULL
                               THEN CONCAT(DATA_TYPE, '(', NUMERIC_PRECISION, ')')
                               ELSE DATA_TYPE
                           END AS FULL_DATA_TYPE
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                    ORDER BY ORDINAL_POSITION
                """, (Config.DB_NAME, table_name))
                
                columns = cursor.fetchall()
                
                if not columns:
                    self.logger.error(f"表 '{table_name}' 不存在或没有列")
                    return {}
                
                # 构建表结构字典
                table_structure = {}
                for column in columns:
                    column_name, data_type, full_data_type = column
                    table_structure[column_name] = full_data_type
                
                self.logger.info(f"成功获取表 '{table_name}' 的结构，共 {len(table_structure)} 个字段")
                return table_structure
                
        except Exception as e:
            self.logger.error(f"获取表结构失败: {e}")
            return {}
    
    def get_max_id(self, table_name: str, id_column: str = 'id') -> int:
        """获取表的最大id值，如果没有则返回0"""
        if not self.connection:
            self.logger.error("数据库未连接")
            return 0
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT MAX(`{id_column}`) FROM `{table_name}`")
                result = cursor.fetchone()
                max_id = result[0] if result and result[0] is not None else 0
                self.logger.info(f"表 '{table_name}' 当前最大id为: {max_id}")
                return int(max_id)
        except Exception as e:
            self.logger.error(f"获取表最大id失败: {e}")
            return 0 