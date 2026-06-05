from datetime import datetime

from sqlalchemy import Integer, DateTime, Index, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.news import News
from models.users import User


class Base(DeclarativeBase):
    pass


class History(Base):
    """
    浏览历史表
    """
    __tablename__ = "history"

    __table_args__ = (
        Index("fk_history_news_idx", "news_id"),
        Index("fk_history_user_idx", "user_id"),
        Index("idx_view_time", "view_time")
    )

    # 知识点：外键级联 ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE")；
    # 他解决的是 关联的外键表中的某一条数据被删除时，当前表格怎么改变的问题，默认情况下报错，这里的修改则表示主键被删除或更新，当前的键跟着删除或更新：
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, comment="历史ID", primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id, ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False, comment="新闻ID")
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="浏览时间")

    def __repr__(self):
        return f"History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})"


















