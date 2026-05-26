from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message: str = "success", data=None):
    """
    返回成功响应结果
    作用：将传入的任何对象(FastAPI, Pydantic, ORM 对象) 转换为正常响应的 json 数据形式
    message: 响应成功返回的信息
    data: 响应给前端的数据
    """
    # 疑问：既然已经可以直接使用字典传入data，转换成json返回结果了，为什么还要而外地写
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    json_response = JSONResponse(content=jsonable_encoder(content))
    return json_response





















