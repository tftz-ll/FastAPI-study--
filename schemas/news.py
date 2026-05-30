from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class NewsBase(BaseModel):
    content: str = Field(..., description="新闻内容")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class NewsInfo(BaseModel):
    """
    新闻类型
    """
    id: int = Field(..., description="新闻ID")
    title: str = Field(..., max_length=255, description="新闻标题")
    description: str = Field(..., max_length=500, description="新闻简介")
    image: str = Field(..., max_length=255, description="封面图片URL")
    author: str = Field(..., max_length=50, description="作者")
    publish_time: datetime = Field(..., description="发布时间", alias="publishTime")
    category_id: int = Field(..., description="分类ID", alias="categoryId")
    views: int = Field(..., description="浏览量")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )



















