import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """项目配置类"""
    
    # 数据库配置
    DB_HOST = os.getenv('DB_HOST', '')
    DB_PORT = int(os.getenv('DB_PORT', ))
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', '')
    DB_CHARSET = os.getenv('DB_CHARSET', 'utf8mb4')
    
    # Excel配置
    EXCEL_START_ROW = 2  # 从第二行开始读取数据
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO') 