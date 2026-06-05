from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud.history import add_history_news, get_history_news_list, delete_history_by_id, check_history, \
    update_history_news, clear_history_news
from models.users import User
from schemas.history import HistoryAddRequest, HistoryTable, HistoryNewsListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(
    prefix="/api/history",
    tags=["history"]
)


# 添加浏览历史记录
@router.post("/add")
async def add_history(
        data: HistoryAddRequest,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
):
    # pydantic对象接收参数【建立pydantic模型】 -》 先检查数据库中是否存在该数据 ->curd进行数据库添加操作【要建立ORM表】-》返回pydantic包装的数据格式【建立pydantic模型】
    is_added = await check_history(news_id=data.news_id, user_id=user.id, db=db)
    if is_added is None:
        added_history_news = await add_history_news(news_id=data.news_id, user_id=user.id, db=db)
    else:
        added_history_news = await update_history_news(news_id=data.news_id, user_id=user.id, db=db)
    response_data = HistoryTable.model_validate(added_history_news)
    return success_response(message="添加成功", data=response_data)


# 获取浏览历史记录列表
@router.get("/list")
async def get_history_list(
        user: User = Depends(get_current_user),
        page: int = Query(1),
        pagesize: int = Query(10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db)
):
    # 接收参数 -》传入skip和pagesize给 crud中的函数获取列表 -》通过pydantic模型返回响应结果【大部分的模型写过，再组装一下即可】
    skip = (page - 1) * pagesize
    news_row, total = await get_history_news_list(skip=skip, pagesize=pagesize, user_id=user.id, db=db)
    has_more = skip + len(news_row) < total
    news_list = [{
        "id": news.id,
        "title": news.title,
        "description": news.description,
        "image": news.image,
        "author": news.author,
        "publishTime": news.publish_time,
        "categoryId": news.category_id,
        "views": news.views,
        "viewTime": view_time
      } for news, view_time in news_row]
    response_data = HistoryNewsListResponse(news_list=news_list, total=total, has_more=has_more)
    return success_response(message="success", data=response_data)


# 删除单挑浏览记录
@router.delete("/delete/{history_id}")
async def delete_history(
        history_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await delete_history_by_id(news_id=history_id, user_id=user.id, db=db)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未存有该浏览记录"
        )
    # 接收浏览记录id -》传入crud中的函数进行删除 -》返回删除条数进行判断
    return success_response(message="删除成功", data=None)


@router.delete("/clear")
async def clear_history(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    # 接收用户id —》根据用户id在curd中删除所有相关数据，返回结果
    delete_num = await clear_history_news(user_id=user.id, db=db)
    return success_response(message="清空成功", data=None)


