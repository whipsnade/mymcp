import pandas as pd
import logging
from typing import List, Dict, Any, Tuple
from config import Config

class ExcelProcessor:
    """Excel数据处理类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def read_excel(self, file_path: str, sheet_name: str | None = None) -> pd.DataFrame | None:
        """读取Excel文件"""
        try:
            # 读取Excel文件，第一行作为列名，从第二行开始读取数据
            result = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                header=0,  # 第一行作为列名
                skiprows=0  # 不跳过任何行，让pandas自动处理
            )
            
            # 如果sheet_name为None，pandas会返回第一个工作表
            if isinstance(result, dict):
                # 如果有多个工作表，取第一个
                df = list(result.values())[0]
            else:
                df = result
                
            self.logger.info(f"成功读取Excel文件: {file_path}")
            # 打印Excel文件中的列名
            self.logger.info(f"Excel文件中的列名: {list(df.columns)}")
            self.logger.info(f"Excel文件中的数据行数: {len(df)}")
            
            # 添加详细的列名调试信息
            self.logger.info("=== Excel列名详细信息 ===")
            for i, col in enumerate(df.columns):
                self.logger.info(f"列 {i+1}: '{col}' (类型: {type(col)}, 长度: {len(str(col))}, 编码: {col.encode('utf-8') if isinstance(col, str) else 'N/A'})")
            
            return df
        except Exception as e:
            self.logger.error(f"读取Excel文件失败: {e}")
            return None
    
    def add_auto_id_column(self, df: pd.DataFrame, start_id: int = 1) -> pd.DataFrame:
        """如果Excel没有id列，自动添加自增长的id列，支持自定义起始id"""
        if df is None or df.empty:
            return df
        
        # 检查是否存在id列（不区分大小写）
        id_columns = [col for col in df.columns if str(col).lower() in ['id', 'id_', '_id']]
        
        if not id_columns:
            # 没有id列，添加自增长的id列
            df_with_id = df.copy()
            id_values = pd.Series(range(start_id, start_id + len(df_with_id)), index=df_with_id.index)
            df_with_id.insert(0, 'id', id_values)
            self.logger.info(f"Excel文件没有id列，已自动添加自增长的id列，起始值为{start_id}")
            return df_with_id
        else:
            # 已有id列，检查是否需要重新编号
            id_col = id_columns[0]
            is_empty = df[id_col].isna().all() or (df[id_col].astype(str).str.strip() == '').all()
            if is_empty:
                # id列全为空，重新编号
                df_with_id = df.copy()
                id_values = pd.Series(range(start_id, start_id + len(df_with_id)), index=df_with_id.index)
                df_with_id[id_col] = id_values
                self.logger.info(f"Excel文件的id列 '{id_col}' 为空，已重新编号，起始值为{start_id}")
                return df_with_id
            else:
                # id列有值，保持原样
                self.logger.info(f"Excel文件已有id列 '{id_col}'，保持原值")
                return df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清理数据，处理空字符"""
        if df is None or df.empty:
            return df
        
        # 复制数据框避免修改原始数据
        cleaned_df = df.copy()
        
        # 处理空字符和空值
        for column in cleaned_df.columns:
            # 将空字符串转换为None
            cleaned_df[column] = cleaned_df[column].replace('', None)
            
            # 将只包含空格的字符串转换为None
            cleaned_df[column] = cleaned_df[column].apply(
                lambda x: None if isinstance(x, str) and x.strip() == '' else x
            )
            
            # 处理NaN值
            cleaned_df[column] = cleaned_df[column].where(pd.notna(cleaned_df[column]), None)
        
        self.logger.info(f"数据清理完成，共处理{len(cleaned_df)}行数据")
        return cleaned_df
    
    def validate_data_types(self, df: pd.DataFrame, table_structure: Dict[str, str]) -> bool:
        """验证数据类型是否与表结构匹配"""
        if df is None or df.empty:
            return True
        
        # 添加调试信息
        self.logger.info("=== 开始验证数据类型 ===")
        self.logger.info(f"Excel中的列名: {list(df.columns)}")
        self.logger.info(f"数据库表结构中的列名: {list(table_structure.keys())}")
        
        # 检查每个Excel列名的详细信息
        for col in df.columns:
            self.logger.info(f"Excel列名: '{col}' (类型: {type(col)}, 长度: {len(str(col))})")
        
        # 检查每个数据库列名的详细信息
        for col in table_structure.keys():
            self.logger.info(f"数据库列名: '{col}' (类型: {type(col)}, 长度: {len(str(col))})")
        
        missing_columns = []
        for column, expected_type in table_structure.items():
            self.logger.info(f"检查列 '{column}' 是否在Excel中存在...")
            if column not in df.columns:
                missing_columns.append(column)
                self.logger.error(f"列 '{column}' 在Excel中不存在")
                # 尝试模糊匹配
                similar_columns = [col for col in df.columns if column.lower() in col.lower() or col.lower() in column.lower()]
                if similar_columns:
                    self.logger.error(f"找到相似的列名: {similar_columns}")
                else:
                    # 尝试部分匹配
                    partial_matches = []
                    for col in df.columns:
                        if any(word in col.lower() for word in column.lower().split()) or any(word in column.lower() for word in col.lower().split()):
                            partial_matches.append(col)
                    if partial_matches:
                        self.logger.error(f"找到部分匹配的列名: {partial_matches}")
            else:
                self.logger.info(f"✅ 列 '{column}' 在Excel中存在")
        
        if missing_columns:
            self.logger.error(f"以下列在Excel中不存在: {missing_columns}")
            self.logger.error(f"Excel中所有列名: {list(df.columns)}")
            self.logger.error("请检查Excel文件格式或数据库表结构是否匹配")
            return False
        
        self.logger.info("数据类型验证通过")
        return True
    
    def convert_to_tuples(self, df: pd.DataFrame, columns: List[str]) -> List[tuple]:
        """将DataFrame转换为元组列表"""
        if df is None or df.empty:
            return []
        
        # 确保列的顺序与传入的columns参数一致
        df_subset = df[columns]
        
        # 转换为元组列表
        data_tuples = []
        for _, row in df_subset.iterrows():
            # 将每行转换为元组，处理None值
            row_tuple = tuple(None if pd.isna(value) else value for value in row)
            data_tuples.append(row_tuple)
        
        self.logger.info(f"成功转换{len(data_tuples)}行数据为元组格式")
        return data_tuples
    
    def get_column_names(self, df: pd.DataFrame) -> List[str]:
        """获取列名列表"""
        if df is None:
            return []
        return df.columns.tolist()
    
    def process_excel_file(self, file_path: str, table_structure: Dict[str, str], 
                          sheet_name: str | None = None, start_id: int = 1) -> Tuple[List[str], List[tuple]] | None:
        """处理Excel文件的完整流程，支持自定义id起始值"""
        # 读取Excel文件
        df = self.read_excel(file_path, sheet_name)
        if df is None:
            return None
        
        # 添加自动id列（如果需要）
        df_with_id = self.add_auto_id_column(df, start_id=start_id)
        
        # 验证数据类型
        if not self.validate_data_types(df_with_id, table_structure):
            return None
        
        # 清理数据
        cleaned_df = self.clean_data(df_with_id)
        
        # 获取列名
        columns = self.get_column_names(cleaned_df)
       
        # 转换为元组列表
        data_tuples = self.convert_to_tuples(cleaned_df, columns)
        
        return columns, data_tuples 