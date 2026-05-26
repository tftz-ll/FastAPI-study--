from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.users import get_user_by_token
from config.db_conf import get_db


# 整合根据token查用户，返回用户的功能
async def get_current_user(authorization: str = Header(..., alias="Authorization"),
                           db: AsyncSession = Depends(get_db)):
    """
    根据请求头参数验证 并获取用户信息
    :param authorization: 请求头参数
    :param db: 数据库会话（已经有了）
    :return: user / raise error
    """
    # 请求头的形状（纯文本的键值对）：
    #   POST /api/user/login HTTP/1.1
    #   Host: 127.0.0.1:8000
    #   Content-Type: application/json
    #   Authorization: Bearer eyJhbGciOi...  我们要的
    #   User-Agent: Mozilla/5.0...
    #   Content-Length: 56
    token = authorization.replace("Bearer", "")  # 因此我们先分割，再获取
    user = await get_user_by_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌或已过期的令牌"
        )
    return user




















