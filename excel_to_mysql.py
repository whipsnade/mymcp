import logging
import os
from typing import Dict, List, Optional
from database import DatabaseManager
from excel_processor import ExcelProcessor
from config import Config

class ExcelToMySQL:
    """Excel到MySQL数据导入主类"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.excel_processor = ExcelProcessor()
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('excel_to_mysql.log', encoding='utf-8')
            ]
        )
    
    def import_excel_to_mysql(self, table_name: str, excel_file_path: str, 
                             table_structure: Optional[Dict[str, str]] = None, 
                             sheet_name: Optional[str] = None) -> bool:
        """
        将Excel数据导入MySQL数据库
        
        Args:
            table_name: 表名
            excel_file_path: Excel文件路径或URL
            table_structure: 表结构字典（可选，如果不提供则从数据库获取）
            sheet_name: 工作表名称（可选）
        
        Returns:
            bool: 导入是否成功
        """
        try:
            # 验证参数
            if not self._validate_parameters(table_name, excel_file_path):
                return False
            
            # 连接数据库
            if not self.db_manager.connect():
                return False
            
            # 如果没有提供表结构，从数据库获取
            if table_structure is None:
                table_structure = self.db_manager.get_table_structure(table_name)
                if not table_structure:
                    self.logger.error(f"无法获取表 '{table_name}' 的结构")
                    return False
                self.logger.info(f"从数据库获取到表结构: {table_structure}")
            
            # 获取数据库当前最大id
            max_id = 0
            id_column = None
            for col in table_structure:
                if col.lower() == 'id':
                    id_column = col
                    break
            if id_column:
                max_id = self.db_manager.get_max_id(table_name, id_column)
            start_id = max_id + 1

            # 处理Excel文件
            result = self.excel_processor.process_excel_file(excel_file_path, table_structure, sheet_name, start_id=start_id)
            if result is None:
                self.logger.error("处理Excel文件失败")
                return False
            
            columns, data_tuples = result
            
            # 插入数据
            if not self.db_manager.insert_data(table_name, columns, data_tuples):
                self.logger.error("插入数据失败")
                return False
            
            self.logger.info(f"成功导入{len(data_tuples)}条记录到表 '{table_name}'")
            return True
            
        except Exception as e:
            self.logger.error(f"导入过程中发生错误: {e}")
            return False
        finally:
            # 断开数据库连接
            self.db_manager.disconnect()
    
    def import_markdown_to_mysql(self, table_name: str, table_structure: Dict[str, str],
                                columns: list, data_rows: list) -> bool:
        """
        将Markdown数据导入MySQL数据库
        
        Args:
            table_name: 表名
            table_structure: 表结构字典
            columns: 列名列表
            data_rows: 数据行列表（元组格式）
        
        Returns:
            bool: 导入是否成功
        """
        try:
            # 验证参数
            if not table_name or not columns or not data_rows:
                self.logger.error("参数不能为空")
                return False
            
            # 连接数据库
            if not self.db_manager.connect():
                return False
            
            # 验证列名是否在表结构中
            missing_columns = [col for col in columns if col not in table_structure]
            if missing_columns:
                self.logger.warning(f"以下列在数据库表中不存在: {missing_columns}")
            
            # 插入数据
            if not self.db_manager.insert_data(table_name, columns, data_rows):
                self.logger.error("插入数据失败")
                return False
            
            self.logger.info(f"成功导入{len(data_rows)}条记录到表 '{table_name}'")
            return True
            
        except Exception as e:
            self.logger.error(f"导入过程中发生错误: {e}")
            return False
        finally:
            # 断开数据库连接
            self.db_manager.disconnect()
    
    def _validate_parameters(self, table_name: str, excel_file_path: str) -> bool:
        """验证输入参数"""
        # 验证表名
        if not table_name or not table_name.strip():
            self.logger.error("表名不能为空")
            return False
        
        # 验证Excel文件路径或URL
        if not excel_file_path:
            self.logger.error("Excel文件路径不能为空")
            return False
        
        # 如果是URL，不需要检查文件是否存在
        if excel_file_path.startswith(('http://', 'https://')):
            return True
        
        # 如果是本地文件，检查是否存在
        if not os.path.exists(excel_file_path):
            self.logger.error(f"Excel文件不存在: {excel_file_path}")
            return False
        
        # 验证文件扩展名
        if not excel_file_path.lower().endswith(('.xlsx', '.xls')):
            self.logger.error("文件必须是Excel格式 (.xlsx 或 .xls)")
            return False
        
        return True
    
    def get_import_summary(self, table_name: str, data_count: int) -> str:
        """生成导入摘要"""
        return f"""
导入摘要:
- 表名: {table_name}
- 导入记录数: {data_count}
- 状态: 成功
        """.strip() 