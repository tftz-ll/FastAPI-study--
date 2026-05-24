from fastapi import APIRouter, Depends, Query, HTTPException
from config.db_conf import get_db
from crud import news

# 创建AIPIRouter实例
# 模块化路由，将不同的路由进行功能的细分，实际使用时再挂载到 main:app上运行
# prefix 路由前缀，具体看API 接口规范文档
router = APIRouter(prefix="/api/news", tags=["news"])

# 接口实现流程
# 1. 定义模块化路由 -》参照 API 接口文档
# 2. 定义模型类 -》数据库表(数据库设计文档)
# 3. 在 crud 文件夹中，封装操作数据库的方法
# 4. 在路由处理函数里面调用 crud 封装好的方法，响应结果；


@router.get("/categories")
async def get_categories(db=Depends(get_db), skip: int = 0, limit: int = 100):
    # 获取数据库中的新闻分类数据 ORM
    # 1. 要有模型类：models中定义
    # 2. 要有查询数据库的方法：crud中封装；
    # 由于数据量较小，当前的分页计算还没有必要，因此不写, 直接返回一百条数据
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "messages": "获取新闻分类成功",
        "data": categories
    }


@router.get("/list")
async def get_news_list(
        db=Depends(get_db),
        category_id: int = Query(..., alias="categoryId"),  # Query还能声明别名，惊了
        page: int = Query(1),
        pagesize: int = Query(10, alias="pageSize", le=100)
):
    # 三个资料-来自于api接口规范文档
    # 1. 新闻列表的获取
    # 2. 新闻总量
    # 3. 是否更多的判断：
    # 此外还要实现分页规则的处理（接口这里直接处理）
    skip_num = (page - 1) * pagesize  # 跳过页数
    news_list = await news.get_news_list(db, category_id, skip_num, pagesize)
    total = await news.get_news_count(db=db, category_id=category_id)

    # 跳过的数量加上当前页面数量 < 总量，则能够加载更多
    has_more = (skip_num + len(news_list)) < total
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }


@router.get("/detail")
async def get_news_detail(db=Depends(get_db), news_id: int = Query(..., alias="id")):
    # 新闻信息可以直接返回 使用id查询
    news_detail = await news.get_news_detail(db=db, news_id=news_id)
    if not news_detail:
        raise HTTPException(
            status_code=404,
            detail="新闻不存在"
        )
    # 每次打开浏览需要将新闻数据的浏览量（view）加一 每次调用这个方法的时候直接+1即可实现
    views_update = await news.increase_news_views(db, news_detail.id)
    if not views_update:
        raise HTTPException(
            status_code=404,
            detail="新闻不存在"
        )  # 这里的异常处理是数据库查询操作的惯常性写法，如果id错误通常在上一个异常处理中就会进行拦截

    # relateNews模：同分类 id 的新闻；
    related_news_list = await news.get_related_news(db, news_detail.id, news_detail.category_id, 5)

    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news_list
            }
    }




















