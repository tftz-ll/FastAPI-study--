from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
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
    id: int
    username: str

    model_config = ConfigDict(
        populate_by_name=True,  # 让 alias和字段名兼容
        from_attributes=True  # 允许 ORM 对象属性中取值
    )


class UserAuthResponse(BaseModel):
    """
    寄存返回的userdata数据
    """
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # 让 alias和字段名兼容
        from_attributes=True  # 允许 ORM 对象属性中取值
    )




