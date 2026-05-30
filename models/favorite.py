import datetime

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, DateTime, Index, ForeignKey, UniqueConstraint

from models.news import News
from models.users import User


class Base(DeclarativeBase):
    pass


class Favorite(Base):
    __tablename__ = "favorite"

    __table_args__ = (
        Index("fk_favorite_news_idx", "news_id"),
        Index("fk_favorite_user_idx", "user_id"),
        UniqueConstraint("user_id", "news_id", name="user_news_unique")
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="收藏ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now, nullable=False, comment="收藏时间")

    def __repr__(self):
        return f"<Favorite>(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, create_at={self.created_at})"


