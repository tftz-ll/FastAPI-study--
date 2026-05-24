from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.news import Category, News


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # skip_page_num = (page - 1) * page_size
    # select(模型名).offset(跳过数量).limit(返回记录数)
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()  # 提取结果
    return categories


async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 查询指定分类下的所有新闻
    # 查询条件：类别id，返回所有
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news = result.scalars().all()
    return news


async def get_news_count(db: AsyncSession, category_id: int):
    # 查询指定id分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    category_cnt = result.scalar_one()  # 只返回一个结果，否则报错，
    return category_cnt


async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news_detail = result.scalar_one_or_none()
    return news_detail


async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 数据库更新，一般要检查数据库是否真的命中了数据
    return result.rowcount > 0


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

