import fastapi
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from utils.exception import *


def register_exception_handler(app: fastapi.FastAPI):
    """
    全局异常处理规则： 子类在前，父类在后， 具体在前，抽象在后
    """
    app.add_exception_handler(HTTPException, http_exception_handler)  # 业务层
    app.add_exception_handler(IntegrityError, integrity_error_handler)  # 数据完整性约束
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)  # 数据库
    app.add_exception_handler(Exception, general_exception_handler)  # 兜底
