from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
import os


# 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:" + os.getenv("mysql_key") + "@localhost:3306/news_app?charset=utf8mb4"
async_engine = create_async_engine(
    url=ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

# 创建异步会话工厂 连接数据表会话

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# 创建依赖项 获取数据库会话数据 让我们能够在路由中操作数据库

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()











