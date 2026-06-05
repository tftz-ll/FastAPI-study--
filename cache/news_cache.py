# 新闻相关的缓存方法：新闻分类的读取和写入
# 根据旁路策略，每一个关于数据库的操作都应当
# 1-尝试从缓存中获取数据
# 2-若没获取到则写入数据
#
# 因此：每一个关于到数据读写的操作都有对应的缓存方法
# 数据获取-数据写入；
from typing import Any, Dict, List

from utils.cache import get_json_cache, set_cache

# 设置键名
CATEGORIES_KEY = "news:categories"


# 获取新闻分类缓存
async def get_cached_categories():
    """
    无传入值
    :return: 新闻分类列表
    """
    cache = await get_json_cache(CATEGORIES_KEY)
    return cache


# 写入新闻分类缓存  data: list[dict[str, Any]] 和 data: List[Dict[str, Any]] 这两个写法有什么区别吗?
# 常用的过期时间：
#   分类、配置 7200
#   列表数据 600
#   详情 1800
#   验证码 120
# 数据越稳定、缓存越持久；
async def set_cache_categories(data: List[Dict[str, Any]], expire: int = 7200):
    cache = await set_cache(key=CATEGORIES_KEY, value=data, expire=expire)
    return cache



















