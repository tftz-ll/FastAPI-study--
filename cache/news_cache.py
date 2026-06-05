# 新闻相关的缓存方法：新闻分类的读取和写入
# 根据旁路策略，每一个关于数据库的操作都应当
# 1-尝试从缓存中获取数据
# 2-若没获取到则写入数据
#
# 因此：每一个关于到数据读写的操作都有对应的缓存方法
# 数据获取-数据写入；
from typing import Any, Dict, List, Optional

from utils.cache import get_json_cache, set_cache

# 设置键名
CATEGORIES_KEY = "news:categories"
NEWS_LIST_KEY_PREFIX = "news:list"
NEWS_DETAIL_KEY_PREFIX = "news:detail"


# 获取新闻分类缓存
async def get_cache_categories():
    """
    无传入值
    :return: 值 / None
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
    """
    设置缓存数据
    :param data: 数据 List[Dict[str, Any]]
    :param expire: 过期时间 s 默认两小时
    :return: True / False
    """
    cache = await set_cache(key=CATEGORIES_KEY, value=data, expire=expire)
    return cache


# 获取新闻列表获取缓存的方法
async def get_cache_news_list(categories: Optional[int], page: int, pagesize: int):
    """
    获取新闻列表缓存
    :param categories: 新闻分类目录
    :param page: 当前页码
    :param pagesize: 页码尺寸
    :return: 值 / None
    """
    categories = categories if categories is not None else "all"
    key = f"{NEWS_LIST_KEY_PREFIX}:{categories}:{page}:{pagesize}"
    cache_data = await get_json_cache(key)
    return cache_data


# 写入新闻列表获取缓存的方法 key: news:list分类id:page:pagesize
async def set_cache_news_list(categories: Optional[int], page: int, pagesize: int,
                              data: list[dict[str, Any]], expire: int = 1800):
    """
    新闻列表获取缓存
    :param categories: 新闻分类目录
    :param page: 当前页码
    :param pagesize: 页码尺寸
    :param data: 数据-不是 ORM 对象
    :param expire: 过期时间
    :return: True / False
    """
    categories = categories if categories is not None else "all"
    key = f"{NEWS_LIST_KEY_PREFIX}:{categories}:{page}:{pagesize}"
    set_cache_status = await set_cache(key=key, value=data, expire=expire)
    return set_cache_status


# 获取新闻详情 key = news:detail: 新闻id
async def get_cache_news_detail(news_id: int):
    """
    获取新闻详情
    :param news_id:
    :return:
    """
    key = f"{NEWS_DETAIL_KEY_PREFIX}:{news_id}"
    cache_data = await get_json_cache(key)
    return cache_data


# 写入新闻详情
async def set_cache_news_detail(news_id: int, data: dict, expire: int = 900):
    """
    写入新闻详情
    :param news_id: 新闻id
    :param data: 数据
    :param expire: 过期时间 默认15分钟
    :return: True / False
    """
    key = f"{NEWS_DETAIL_KEY_PREFIX}:{news_id}"
    cache_satus = await set_cache(key=key, value=data, expire=expire)
    return cache_satus











