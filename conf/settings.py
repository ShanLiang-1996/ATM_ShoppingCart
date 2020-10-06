"""
用于存放项目配置信息
"""
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

USER_DATA_DIR = os.path.join(BASE_DIR, 'db', 'user_data')
