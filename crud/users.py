# 根据用户名获取用户
import datetime
import uuid

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.user import UserRequest, UserUpdateRequest
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


# 用户登入逻辑
async def authenticate_user(db: AsyncSession, username: str, password: str):
    """
    验证用户是否存在
    :param db: db
    :param username: 用户名
    :param password: 密码（明文）
    :return: user / None
    """
    user = await get_user_by_username(db, username)
    if not user:
        # 用户不存在
        return None
    if not security.verify_password(password, user.password):
        # 密码不正确
        return None
    return user


# 根据token查用户
async def get_user_by_token(db: AsyncSession, token: str):
    """
    验证用户登入状态
    :param db:
    :param token: token
    :return: None / user_id
    """
    # 根据token查用户
    smtm = select(UserToken).where(UserToken.token == token)
    result = await db.execute(smtm)
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.datetime.now():
        # token不存在或者是token过期了
        return None

    # 根据token获取user
    smtm = select(User).where(User.id == db_token.user_id)
    result = await db.execute(smtm)
    user = result.scalar_one_or_none()
    return user


# 更新用户信息
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    """
    更新用户信息
    :param db: 数据库session
    :param username:  用户名
    :param user_data:  请求体参数 UserUpdateRequest
    :return: raise error / updated_user
    """
    # 新知识：
    # 传入的user_data是pydantic类型
    # Orm 语句中value需要的是 key=value的形式
    # 我们的方法：将pydantic转为字典，再使用 ** 的方式解包出来；
    smtm = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True  # 这两个参数的意义：保证只有设置了值的userdata字段才会提交到数据库中
        ))
    result = await db.execute(smtm)
    await db.commit()

    # 检查更新
    if result.rowcount == 0:  # type: ignore # 提醒pycharm忽略这个属性，不然有黄线
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    # 获取更新后的用户
    updated_user = await get_user_by_username(db, username)
    return updated_user


# 修改密码: 验证 -》加密 -》修改
async def update_password_process(db: AsyncSession, user: User, old_password: str, new_password: str):
    """
    密码更新操作
    :param db:  数据库会话 
    :param user:  用户模型对象
    :param old_password: 旧密码
    :param new_password: 新密码
    :return: True /False
    """
    result = security.verify_password(old_password, user.password)
    if not result:
        return False

    hash_password = security.get_hash_password(new_password)
    stmt = update(User).where(User.username == user.username).values(password=hash_password)

    await db.execute(stmt)
    await db.commit()
    await db.refresh(user)
    return True











