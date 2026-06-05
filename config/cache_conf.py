import redis.asyncio as aredis

# 变量储存是因为可能会使用到代理服务器等等操作导致端口号等信息产生变化，存变量方便修改
# 更进一步的写法是放到yaml中存放【例如AgentUnit】

"""
缓存操作就是围绕Redis 作 存、取、删、判断、过期、等操作，让数据访问更快，数据库压力更小
redis 存储数据形式：key-value

setex()  设置缓存指定过期时间
get()  获取缓存值，不存在返会None
delete()  删除指定的缓存键
exists()  检查缓存键是否存在，返回布尔值
"""

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
# 创建 Redis 连接对象

redis_client = aredis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,   # 将字节数据解码为字符串
    protocol=2
)


# 无论是字符串还是列表，直接存，取出来的时候手动解析，避免python解析负担















