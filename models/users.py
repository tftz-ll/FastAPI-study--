from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, DateTime, String, Enum, Index, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, comment="用户ID")


class User(Base):
    """
    用户信息表 ORM模型
    注：建表过程中的参数细节是根据数据库响应表的ddl对照而来的 （右上角）
    """
    __tablename__ = "user"

    # 创建索引
    __table_args__ = (
        Index("username_UNIQOE", "username"),
        Index("phone_UNIQUW", "phone")
    )

    username: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=True, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment="用户密码(加密)")
    nickname: Mapped[Optional[str]] = mapped_column(String(50), comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), comment="头像url",
                                                  default="")
    gender: Mapped[Optional[str]] = mapped_column(Enum("male", "female", "unknown"), default="unknown", comment="性别")
    bio: Mapped[Optional[str]] = mapped_column(String(500), comment="个人简介", default="这个人很懒，什么也没有写...")
    phone: Mapped[str] = mapped_column(String(20), unique=True, comment="手机号")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return f"<User>(id={self.id}, username={self.username}, gender={self.gender}, phone={self.phone})"


class UserToken(Base):
    """
    用户令牌 ORM 模型
    """
    __tablename__ = 'user_token'

    # 创建索引
    __table_args__ = (
        Index("token_UNIQUE", 'token'),
        Index('fk_user_token_idx', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, comment="令牌id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="关联的用户id")
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment="令牌值")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")

    def __repr__(self):
        return f"<UserToken>(id={self.id}, user_id={self.user_id}, token={self.token})"
























