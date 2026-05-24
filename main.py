from fastapi import FastAPI
from routers import news, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源，开发阶段所有源都可访问，生产环境需要指定源
    allow_credentials=True,  # 允许携带cookies
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"]  # 允许的请求头
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 挂载路由/注册路由
app.include_router(news.router)
app.include_router(users.router)




"""
## 跨域资源共享问题
写好后端代码后，启动前端代码会发现请求被拦截了，这是因为触发了浏览器的CORS机制  
>  CORS：浏览器允许允许在一个源的web应用，通过浏览器项另一个源的服务器发起请求，但获取到资源的前提是 **服务器授权**  
> 
同源的要求: 
1. 协议相同
2. 域名相同
3. 端口号相同

解决方法：
    使用CORS中间件
"""

