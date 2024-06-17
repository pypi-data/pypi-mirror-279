from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from . import settings
from functools import lru_cache

# *********** 数据库连接配置 *********** #
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
    settings.DB_USER, settings.DB_PASSWORD, settings.DB_HOST, settings.DB_PORT, settings.DB_NAME
)

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=settings.DB_POOL_SIZE, pool_recycle=settings.DB_POOL_RECYCLE)
# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 声明基类
Base = declarative_base()


@lru_cache()
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
