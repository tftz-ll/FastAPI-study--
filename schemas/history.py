from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict

from schemas.news import NewsInfo


class HistoryAddRequest(BaseModel):
    """
    浏览历史记录添加请求参数接收
    """
    news_id: int = Field(..., alias="newsId")


class HistoryTable(BaseModel):
    """
    对 history这张表的pydantic模型
    """
    id: int
    user_id: int
    news_id: int
    view_time: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class HistoryNewsList(NewsInfo):
    view_time: datetime = Field(..., alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class HistoryNewsListResponse(BaseModel):
    """
    浏览历史列表响应pydantic对象
    """
    news_list: list[HistoryNewsList] = Field(..., alias="list")
    total: int
    has_more: bool = Field(..., alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )













