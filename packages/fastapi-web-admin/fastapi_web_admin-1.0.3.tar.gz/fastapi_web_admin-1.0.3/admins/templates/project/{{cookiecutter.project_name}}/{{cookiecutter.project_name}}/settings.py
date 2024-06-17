from pathlib import Path

# ------------------------------ 项目目录 ------------------------------#
BASE_DIR = Path(__file__).resolve().parent.parent

TITLE = "{{cookiecutter.project_name}}"
DESCRIPTION = "{{cookiecutter.project_name}} 项目的描述"
VERSION = "V1.0.0"

# ------------------------------ 秘钥配置 ------------------------------#
SECRET_KEY = '{{cookiecutter.secret_key}}'

# ------------------------------ 项目环境 ------------------------------#
DEBUG = True

# ------------------------------ 跨域配置 ------------------------------#
ALLOWED_ORIGINS = ['*']
ALLOWED_HEADERS = ['*']
ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
ALLOWED_CREDENTIALS = True

# ------------------------------ 模版配置 ------------------------------#
TEMPLATES_DIR = BASE_DIR / 'templates'

# ------------------------------ 静态文件 ------------------------------#
STATIC_DIR = BASE_DIR / 'static'
STATIC_URL = '/static/'

# ------------------------------ 数据库配置 ------------------------------#
DB_NAME = "{{cookiecutter.project_name}}_db"  # 数据库名称
DB_HOST = "127.0.0.1"  # 数据库地址
DB_PORT = "3306"  # 数据库端口
DB_USER = "root"  # 数据库用户
DB_PASSWORD = "admin"
DB_POOL_SIZE = 5  # 连接池的大小
DB_POOL_RECYCLE = 3600  # 1小时后 回收连接
