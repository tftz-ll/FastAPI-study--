from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update

from cache.news_cache import get_cache_categories, set_cache_categories, get_cache_news_list, set_cache_news_list, \
    get_cache_news_detail, set_cache_news_detail
from models.news import Category, News


# 获取新闻分类目录[cache]
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # skip_page_num = (page - 1) * page_size
    # select(模型名).offset(跳过数量).limit(返回记录数)

    # 先尝试从缓存中获取数据
    cache_category = await get_cache_categories()
    if cache_category is not None:
        return [Category(**item) for item in cache_category]

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()  # 提取结果

    # 将数据存入缓存
    if categories:
        # 注意！这里获取到的categories是orm对象，需要转换
        json_categories = jsonable_encoder(categories)
        await set_cache_categories(data=json_categories)
    return categories


# 获取新闻列表[cache]
async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 查询指定分类下的所有新闻
    # 查询条件：类别id，返回所有
    # 先尝试从缓存中获取数据
    page = skip // limit + 1
    cache_news_list = await get_cache_news_list(category_id, page=page, pagesize=limit)
    if cache_news_list is not None:
        return [News(**item) for item in cache_news_list]

    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    if news_list:
        # 添加数据到数据库
        json_news_list = jsonable_encoder(news_list)
        await set_cache_news_list(category_id, page=page, pagesize=limit, data=json_news_list)
    return news_list


# 获取新闻数量[None cache]
async def get_news_count(db: AsyncSession, category_id: int):
    # 查询指定id分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    category_cnt = result.scalar_one()  # 只返回一个结果，否则报错，
    return category_cnt


# 获取新闻详情[cache]
async def get_news_detail(db: AsyncSession, news_id: int):
    # 缓存中获取
    cache_data = await get_cache_news_detail(news_id=news_id)
    if cache_data is not None:
        return News(**cache_data)

    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news_detail = result.scalar_one_or_none()
    # 存入缓存
    if news_detail:
        js_news_detail = jsonable_encoder(news_detail)
        await set_cache_news_detail(news_id=news_id, data=js_news_detail)
    return news_detail


# 增加新闻浏览数量[cache好像没必要-每次查看一次就更新缓存和数据库没用还增加负担] - 关联新闻详情缓存
async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 数据库更新，一般要检查数据库是否真的命中了数据
    return result.rowcount > 0


# 获取相关新闻
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc()  # decrease 降序排序，
    ).limit(limit)  # 根据前几名浏览量和发布时间进行排序
    result = await db.execute(stmt)
    related_news_list = result.scalars().all()
    # 将数据库中的数据进行过滤，去掉不需要的数据（虽然暂时没有）
    news = [{
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news_list
            } for news_detail in related_news_list]
    return related_news_list

