from fastapi import HTTPException
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.favorite import Favorite
from models.news import News


# 根据newsID查询收藏状态
async def check_favorite_by_news_id(news_id: int, user_id: int, db: AsyncSession):
    """
    根据新闻id查询新闻收藏状态
    :param news_id:
    :param user_id:
    :param db:
    :return:
    """
    stmt = select(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user_id)
    result = await db.execute(stmt)
    favorite_status = result.scalar_one_or_none() is not None
    return favorite_status


# 添加收藏
async def add_news_favorite(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    """

    :param db: 数据库会话
    :param user_id: 用户id
    :param news_id: 新闻id
    :return: 一个 Favorite ORM对象
    """
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


# 根据user_id 与news_id 查询，删除对应数据
async def delete_news_favorite(
        user_id: int,
        news_id: int,
        db: AsyncSession
):
    """
    收藏新闻删除
    :param user_id: 用户id
    :param news_id: 新闻id
    :param db: 数据库会话
    :return: True / False
    """
    stmt = delete(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount >= 1


# 获取收藏新闻列表 通过用户，page，pagesize查询页面
async def get_favorite_news_list(
        user_id: int,
        db: AsyncSession,
        skip: int = 0,
        pagesize: int = 10,
):
    """
    获取用户收藏列表
    :param user_id: 用户id
    :param skip: 跳过的新闻数目
    :param pagesize: 页面尺寸
    :param db: 数据库会话
    :return: favorite_news_list 新闻列表
    返回的示例:
     [
       (新闻对象, 收藏时间, 收藏id)
     ];
    """
    # 收藏的总量
    stmt = select(func.count()).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    total_num = result.scalar_one()

    # 获取的新闻列表，联表查询 join() + 排序（time） + 分页
    # 联合查询语法
    # stmt = select(主体模型, 副模型【可以是他的字段，可以起别名】).join(联合的查询模型, 联合查询的条件).
    # where(联合后的表的查询条件).order_by()
    # 返回的示例
    # [
    #   (新闻对象, 收藏时间, 收藏id)
    # ];
    stmt = (select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id")).
            join(Favorite, Favorite.news_id == News.id).
            where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc())).offset(skip).limit(pagesize)
    result = await db.execute(stmt)
    rows = result.all()
    return rows, total_num


async def clear_favorite_news_list(
        user_id: int,
        db: AsyncSession
):
    """
    收藏列表情空
    :param user_id: 用户id
    :param db: 数据库会话
    :return: 删除数量
    """
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    delete_num = result.rowcount
    return delete_num



