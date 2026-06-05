import json
from typing import Any

from config.cache_conf import redis_client


# 读取：字符串
async def get_cache(key: str):
    """
    传入键，获得对应的值
    :param key:
    :return: 值 / None
    """
    try:
        cache = await redis_client.get(key)
    except Exception as e:
        # 实际上这些错误处理我应该专门写一个log存放
        print(f"获取缓存失败{e}")
        return None
    return cache


# 读取：列表或字典
async def get_json_cache(key: str):
    """
    传入键，获得对应的值 - 列表或字典
    :param key:
    :return: 值 / None
    """
    try:
        cache = await redis_client.get(key)
        if cache:
            return json.loads(cache)  # 字符串转列表或字典
        return None
    except Exception as e:
        print(f"[get_json_cache] 运行错误，因为{e}")
        return None


# 设置缓存 setex(key, expire, value)
async def set_cache(key: str, value: Any, expire: int = 3600):
    """
    设置缓存
    :param key: 键
    :param value: 值
    :param expire: 过期时间 int 秒
    :return: True / False
    """
    # 实际上对于不同的数据过期时间不一样
    try:
        if isinstance(value, (dict, list)):
            # list或dict转字符串再存
            value = json.dumps(value, ensure_ascii=False)  # 不转换为ascii【让人能看懂】
        await redis_client.setex(key, expire ,value)
        return True
    except Exception as e:
        print(f"[set_cache] 设置缓存失败{e}")
        return False




















