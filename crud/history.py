import datetime

from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def check_history(
        user_id: int,
        news_id: int,
        db: AsyncSession
):
    stmt = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(stmt)
    check = result.scalar_one_or_none()
    return check


async def add_history_news(
        user_id: int,
        news_id: int,
        db: AsyncSession
):
    """
    浏览历史记录添加
    :param user_id: 用户id
    :param news_id: 新闻id
    :param db: 数据库会话
    :return: 添加的ORM对象
    """
    history_news = History(user_id=user_id, news_id=news_id)
    db.add(history_news)
    await db.commit()
    await db.refresh(history_news)
    return history_news


# 更新数据库
async def update_history_news(
        user_id: int,
        news_id: int,
        db: AsyncSession
):
    """
    更新浏览历史
    :param user_id:
    :param news_id:
    :param db:
    :return:
    """
    stmt = (update(History).where(History.user_id == user_id, History.news_id == news_id).
            values(view_time=datetime.datetime.now()))
    result = await db.execute(stmt)
    await db.commit()

    stmt = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(stmt)
    updated_news = result.scalar_one_or_none()
    return updated_news


async def get_history_news_list(
        skip: int,
        pagesize: int,
        user_id: int,
        db: AsyncSession
):
    """
    获取浏览历史列表
    :param skip: 跳过新闻的数目
    :param pagesize: 单页尺寸
    :param user_id: 用户id
    :param db: 数据库会话
    :return: 浏览历史新闻清单， 总数
    """
    # 获取总数
    stmt = select(func.count()).where(History.user_id == user_id)
    result = await db.execute(stmt)
    total = result.scalar_one()

    # 联合查询
    # 记得将获取到的浏览历史记录进行按照时间进行降序排列（后看的在前面）
    stmt = ((select(News, History.view_time).
            join(History, History.news_id == News.id).
            where(History.user_id == user_id)).
            order_by(History.view_time.desc()).
            offset(skip).limit(pagesize))
    result = await db.execute(stmt)
    history_row = result.all()
    return history_row, total


async def delete_history_by_id(
        news_id: int,
        user_id: int,
        db: AsyncSession
):
    """
    删除单挑浏览历史
    :param news_id: 新闻id
    :param user_id: 用户id
    :param db: 数据库会话
    :return: 删除数目 > 0
    """
    stmt = delete(History).where(History.news_id == news_id, History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def clear_history_news(
        user_id: int,
        db: AsyncSession
):
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount












