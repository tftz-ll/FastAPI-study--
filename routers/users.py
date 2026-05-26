from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.users import create_token, authenticate_user, update_user, update_password_process
from models.users import User
from schemas.user import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserChangePassword
from crud import users
from config.db_conf import get_db
from utils.auth import get_current_user
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
    # api接口文档中的data分为token和user_info两个数据
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data=response_data)


@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登入逻辑：检查该用户是否存在 -》检查密码是否正确（hash加密验证） -》生成token -》响应结果返回
    user = await authenticate_user(db, password=user_data.password, username=user_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名和密码错误"
        )
    token = await create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))  # model_validate从数据库中拿取值的意思
    return success_response(message="登入成功", data=response_data)


# 查token -》查用户 -》返回信息
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    """
    由于接口接收到的是请求头，因此我们可以使用依赖注入来直接接收参数
    """
    response_data = UserInfoResponse.model_validate(user)
    return success_response(message="获取个人信息成功", data=response_data)


# 用户信息更新：验证token -》 查找用户 -》更新信息
# 参数： Header、Body（）、db
@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest,
                           user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)
                           ):
    user = await update_user(db, user.username, user_data)

    response_data = UserInfoResponse.model_validate(user)
    return success_response(message="更新用户信息成功", data=response_data)


# 更新密码
@router.put("/password")
async def update_password(password: UserChangePassword,
                          user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)
                          ):
    # 验证旧密码是否正确（validate） -》修改新密码（密码转密文）
    update_password_status = await update_password_process(db, user, password.old_password, password.new_password)
    if not update_password_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="修改密码失败，检查旧密码是否正确"
        )
    response_data = None
    return success_response(message="更新密码成功", data=response_data)




