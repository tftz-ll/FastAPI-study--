from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.news import NewsInfo


# 创建时间需要设置为基础属性，后续响应字段会用到


class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")


class FavoriteAddResponse(BaseModel):
    """
    用户添加收藏响应信息
    """
    id: int = Field(...)
    user_id: int = Field(..., alias="userId")
    news_id: int = Field(..., alias="newsId")
    created_at: datetime = Field(..., alias="createTime")

    model_config = ConfigDict(
        populate_by_name=True,  # 这个配置的设置意思是，响应时有别名就用别名，没有则用字段名，保证了响应数据能够和文档要求对齐
        from_attributes=True
    )


class FavoriteListResponseBase(BaseModel):
    total: int
    has_more: bool = Field(..., alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class FavoriteNewsRows(NewsInfo):
    """
    装新闻列表中的list部分，在下面的模型类中写太难看了，先抽象一个出来
    """
    favorite_time: datetime = Field(..., alias="favoriteTime")


class FavoriteNewsListResponse(FavoriteListResponseBase):
    """
    news_list: 新闻收藏列表
    total: 新闻总数
    has_more: 是否有更多
    """
    news_list: list[FavoriteNewsRows] = Field(..., alias="list")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
























