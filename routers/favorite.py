from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud.favorite import check_favorite_by_news_id, add_news_favorite, delete_news_favorite, get_favorite_news_list, \
    clear_favorite_news_list
from models.users import User
from schemas.favorite import FavoriteAddRequest, FavoriteAddResponse, FavoriteNewsListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


# 检查新闻收藏状态
@router.get("/check")
async def check_favorite(news_id: int = Query(..., alias="newsId"),
                         user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    # 一定要记得先验证用户是否登入
    # 获取用户，news_id 在favorite表中查看新闻收藏状态
    favorite_status = await check_favorite_by_news_id(news_id=news_id, user_id=user.id, db=db)
    response_data = {"isFavorite": favorite_status}
    return success_response(message="success", data=response_data)


# 添加收藏功能
@router.post("/add")
async def add_favorite(
        data: FavoriteAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    is_favorite = await check_favorite_by_news_id(news_id=data.news_id, user_id=user.id, db=db)
    if is_favorite:
        raise HTTPException(
            status_code=400,
            detail="重复收藏"
        )
    favorite_news = await add_news_favorite(db, user.id, data.news_id)
    response_data = FavoriteAddResponse.model_validate(favorite_news)
    return success_response(message="收藏成功", data=response_data)


# 取消收藏
@router.delete("/remove")
async def delete_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    # 传入新闻id -》根据id删除favorite表中新闻数据 -》返回
    delete = await delete_news_favorite(user_id=user.id, news_id=news_id, db=db)
    if not delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该新闻未被收藏"
        )
    return success_response(message="取消收藏成功", data=None)


# 获取收藏列表
@router.get("/list")
async def get_favorite_list(
        page: int = Query(1),
        pagesize: int = Query(10, alias="pageSize", ge=10, le=100),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * pagesize
    news_rows, total = await get_favorite_news_list(user_id=user.id, skip=skip, pagesize=pagesize, db=db)
    has_more = (skip + len(news_rows)) < total
    # 建立pydantic模型用于返回
    favorite_list = [{
        "id": news.id,
        "title": news.title,
        "description": news.description or "",
        "image": news.image or "",
        "author": news.author or "",
        "publish_time": news.publish_time,
        "category_id": news.category_id,
        "views": news.views,
        "favorite_time": favorite_time,
    } for news, favorite_time, _ in news_rows]

    response_data = FavoriteNewsListResponse(news_list=favorite_list, total=total, has_more=has_more)
    return success_response(message="success", data=response_data)


# 收藏列表情况
@router.delete("/clear")
async def clear_favorite_list(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):

    num = await clear_favorite_news_list(user_id=user.id, db=db)
    message = f"成功删除{num}条收藏记录"
    return success_response(message=message, data=None)









