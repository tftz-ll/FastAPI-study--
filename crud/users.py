# 根据用户名获取用户
import datetime
import uuid

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.user import UserRequest
from utils import security


async def get_user_by_username(db: AsyncSession, username: str):
    """
    根据用户名查找用户
    """
    smtm = select(User).where(User.username == username)
    result = await db.execute(smtm)
    user = result.scalar_one_or_none()  # 记得处理用户不存在的情况
    return user


async def create_user(db: AsyncSession, user_data: UserRequest):
    """
    创建新用户：
        加密(使用passlib) -》add
    """
    hash_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hash_password)  # 用模型类创建user
    db.add(user)  # git add
    await db.commit()  # git commit -m"***"
    await db.refresh(user)  # 从数据库读出最新的值，保证数值正确
    return user


async def create_token(db: AsyncSession, user_id: int):
    """
    创建用户token
    有 token: 更新
    无 token: 创建
    """
    # 生成token
    token = str(uuid.uuid4())  # uuid.uuid4()随机生成的哈希值，碰撞概率极低
    # 设置过期时间
    expires_at = datetime.datetime.now() + datetime.timedelta(days=7)  # timedelta 生成时间长度，可用于计算相加
    # 查询是否有token
    smtm = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(smtm)
    existing_token = result.scalar_one_or_none()
    # 更新或创建
    if existing_token:
        # 如果有token，更新
        existing_token.token = token
        existing_token.expires_at = expires_at
    else:
        # 如果没有token，创建
        new_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(new_token)

    await db.commit()
    return token









