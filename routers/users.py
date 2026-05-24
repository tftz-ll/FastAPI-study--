from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.users import create_token
from schemas.user import UserRequest, UserAuthResponse, UserInfoResponse
from crud import users
from config.db_conf import get_db
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(
        user_data: UserRequest,
        db: AsyncSession = Depends(get_db),
):

    # 注册逻辑：验证用户是否存在 -》
    existing_user = await users.get_user_by_username(db, username=user_data.username)
    if existing_user:  # 如果存在用户，抛出异常
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # 表示客户端发送的请求有问题，服务器无法理解或处理
            detail="用户已存在"
        )

    # 创建用户 -》
    user = await users.create_user(db, user_data)

    # 生成Token -》
    token = await create_token(db=db, user_id=user.id)
    # 响应结果
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #                 "id": user.id,
    #                 "username": user.username,
    #                 "bio": user.bio,
    #                 "avatar": user.avatar
    #             }
    #     }
    # }
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=response_data)













