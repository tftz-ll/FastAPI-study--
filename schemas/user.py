from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    # 用户登入时需要携带的两个参数 对应的存放为pydantic类
    username: str
    password: str


# user_info 对应的类: 基础类(可选字段) + Info类 (id, 用户名)
class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像Url")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


class UserInfoResponse(UserInfoBase):
    """
    传入一个用户对象，使用model_valida方法获取到符合响应接口规范的信息形式
    """
    id: int
    username: str

    model_config = ConfigDict(
        populate_by_name=True,  # 让 alias和字段名兼容
        from_attributes=True  # 允许 ORM 对象属性中取值
    )


class UserAuthResponse(BaseModel):
    """
    返回用户响应信息的类
    """
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # 让 alias和字段名兼容
        from_attributes=True  # 允许 ORM 对象属性中取值
    )


class UserUpdateRequest(BaseModel):
    """
    用户信息更新请求
    """
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None


class UserChangePassword(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(..., min_length=6, alias="newPassword", description="新密码")





