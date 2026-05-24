from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, ForeignKey, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 要有什么样的模型基类首先要取决于数据库中有什么字段


class Base(DeclarativeBase):
    """
    news与news_category 两张表中都有的时间字段直接作为模型基类
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )


class Category(Base):
    __tablename__ = "news_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类id")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序")

    def __repr__(self):
        """
        重写方法，打印对象时返回的字符串会变成对应的信息，而不是内存地址
        """
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"


class News(Base):
    __tablename__ = "news"

    # 创建索引：提升查询速度，可以当作添加了一个目录
    __table_args__ = (
        Index("fk_news_category_idx", "category_id"),  # 高频查询场景
        Index("idx_publish_time", "publish_time")  # 按照发布时间排序时用到
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False,  comment="类别id")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻简介")
    content: Mapped[str] = mapped_column(String(500))
    image: Mapped[Optional] = mapped_column(String(255), comment="封面图片url")
    author: Mapped[str] = mapped_column(String(50), comment="作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("news_category.id"), nullable=False, default=1, comment = "类别id")
    views: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="发布日期")

    def __repr__(self):
        return (f"<News(id={self.id}, title={self.title}, description={self.description}, content={self.content}, "
                f"image={self.image}, author={self.author}, category_id={self.category_id}, views={self.views}, "
                f"publisher_time={self.publish_time})>")















