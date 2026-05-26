import traceback

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

# 开发模式：True-返回详细错误信息
# 生产模式：False-返回简化错误信息
DEBUG_MODE = True


# 异常处理函数的作用-
# 1. 统一异常处理信息响应接口
# 2. 全局错误处理，以后不用写错误处理了；
async def http_exception_handler(request: Request, exc: HTTPException):
    """
        处理 HTTPException 异常
        """
    # HTTPException 通常是业务层主动抛出的，data 保持 None，不传送数据出去
    json_response = JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

    return json_response


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    处理数据库完整性约束错误, 好处在于如果以后遇到了新的未加入判断逻辑的错误，只要加进去就行了，可扩展性高
    """
    error_msg = str(exc.orig) if exc.orig else str(exc)  # 这里实际上是把代码错误信息转换成字符串抽取出来了
    # 他的内部类似于
    # (1366, "Incorrect integer value: 'abc' for column 'id' at row 1")
    # (2003, "Can't connect to MySQL server on 'localhost:3306' (10061)")
    # 诸如此类的报错信息，因此可以使用下面的方法进行判断响应；
    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "关联数据不存在"
    else:
        detail = "数据约束冲突，请检查输入"
    # 当前字符串匹配的问题在于换数据库后可能会失效，使用下面这种约束错误码可能更好
    # if exc.orig and exc.orig.args[0] == 1062:  # MySQL 唯一约束错误码
    #     detail = "用户名已存在"
    # 开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": "IntegrityError",
            "error_detail": error_msg,
            "path": str(request.url)
        }

    json_response = JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": detail,
            "data": error_data
        }
    )

    return json_response


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """
    处理 SQLAlchemyError 数据库错误
    """
    # 开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url)
            #  • traceback 是 Python 标准库，用于处理异常堆栈信息
            # • format_exc() 返回当前异常（如果有）的完整堆栈跟踪字符串
        }
    json_response = JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 500,
            "message": "数据库操作失败，请稍后重试",
            "data": error_data
        }
    )

    return json_response


async def general_exception_handler(request: Request, exc: Exception):
    """
    处理所有未捕获的异常
    """
    # 开发者模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            # 格式化信息为字符串，也方便后续进行日志记录和调试
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }

    json_response = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": error_data
        }
    )

    return json_response

































