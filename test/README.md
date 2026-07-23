# 今日头条后端实现（简易版）

## 介绍

__学习用__ : 这是一个简易版今日头条的后端实现，只适用于参考学习

## 拉取到本地

**请确保python版本不低于3.12**

### 1.克隆仓库

```bash
git clone https://github.com/tftz-ll/FastAPI-study--.git
cd FastAPI-study--
```

### 2.安装依赖

```bash
pip install -r requirements.txt
```

### 3.数据库配置

redis、mysql数据库请自行配置

### 4.启动

前端

```powershell
cd FastAPI-study--\项目物料\03-前端项目代码\xwzx-news
npm install
npm run dev
```

后端

```bash
uvicorn main:app --reload
```



## 配置信息

配置信息存放在config文件夹下，由于体量小，并未进一步抽象为json或yaml等形式

```python
# cache_conf.py
# 用于redis的接入使用，请根据个人情况进行修改
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0


# db_conf.py
# 用于sql数据库的接入使用，请根据个人情况进行修改
# mysql 密码从环境变量 mysql_key 读取，也可直接替换为你的密码字符串
ASYNC_DATABASE_URL = "mysql+aiomysql://root:" + os.getenv("mysql_key") + "@localhost:3306/news_app?charset=utf8mb4"
```



## 代码结构

本项目代码将新闻头条的实现拆分为favorite（收藏）、history（历史记录）、news（新闻内容）、user（用户信息）四大分类实现

```text
## 代码结构

├─cache  --各模块缓存加载，优先读 Redis，未命中回源 MySQL
│  │  news_cache.py --实现了新闻内容的缓存加载，加载新闻时将优先从缓存中获取，未获取到则从sql数据库加载，并加入缓存
│
├─config -- redis与mysql环境配置
│  │  cache_conf.py  -- redis配置
│  ├─ db_conf.py -- mysql配置
│
├─crud --分别实现各类信息模块的‘增’、‘删’、‘改’、‘查’等操作，主要的功能模块
│  │  favorite.py -- 新闻收藏的 查询、添加、删除、获取收藏列表、清空收藏列表五大功能的实现
│  |  history.py --历史浏览记录的 查询、添加、更新、获取新闻列表、删除历史新闻、清空浏览记录六大功能的实现
│  │  news.py --新闻信息的 获取新闻分类、获取新闻列表、查看指定分类新闻数量、获取新闻详情、增加新闻浏览数量、相关新闻推荐 六大功能的实现
│  │  news_cache_added.py --news模块的镜像实现，但使用的是redis数据库缓存，而非mysql数据库
│  ├─ users.py --用户模块的 获取用户名、创建用户、创建用户令牌、校验用户登入信息、查询用户、更新用户信息、修改密码 七大功能的实现
│
├─models --收藏/历史浏览/新闻/用户信息的sqlalchemy模板，ORM模型，用于crud中数据库操作
│  │  favorite.py --收藏新闻的sqlalchemy模板
│  │  history.py --历史浏览的sqlalchemy模板
│  │  news.py --新闻的sqlalchemy模板
│  ├─ users.py --用户信息的sqlalchemy模板
│
├─routers --收藏/历史浏览/新闻/用户信息功能路由挂载
│  │  favorite.py --检查收藏/取消收藏/添加收藏/获取收藏列表/清空收藏列表功能路由挂载
│  │  history.py --添加浏览历史记录/获取浏览记录/删除单条浏览记录/清空浏览记录功能挂载
│  │  news.py --获取分类信息/获取新闻列表/获取新闻详情功能路由挂载
│  ├─ users.py --用户注册/用户登入/用户查询/用户信息更新/密码修改功能挂载
│
├─schemas --pydantic模型建立，用于router中路由校验环节
│  │  favorite.py --收藏pydantic模型建立
│  │  history.py --历史浏览记录pydantic模型建立
│  │  news.py --新闻信息pydantic模型建立
│  ├─ user.py --用户信息pydantic模型建立
│
├─test
│   ├─ README.md
│
├─utils --项目中可复用工具的封装
│  │  auth.py --用户信息验证，用于登入
│  │  cache.py --缓存获取，直接连接redis进行加载缓存的实现
│  │  exception.py --全局异常处理响应
│  │  exception_handler.py --全局异常处理规则
│  │  response.py --响应解析，统一响应的数据格式，将传入的任何对象(FastAPI, Pydantic, ORM 对象) 转换为正常响应的 json 数据形式
│  ├─ security.py --用户登入的密码验证封装
|
├─main.py --router注册、运行文件
```

