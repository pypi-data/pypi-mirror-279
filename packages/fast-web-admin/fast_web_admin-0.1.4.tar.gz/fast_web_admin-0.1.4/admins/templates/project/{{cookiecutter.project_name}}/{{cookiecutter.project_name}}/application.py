from fastapi.middleware.cors import CORSMiddleware
from . import settings
from .events import start_up_event, shut_down_event
from fastapi.exceptions import HTTPException, RequestValidationError
from .errors import handle_http_exception, handle_request_exception
from .urls import router
from fastapi import FastAPI


def create_app() -> FastAPI:
    # *********** 创建fastapi实例 *********** #
    app = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        on_startup=[start_up_event],
        on_shutdown=[shut_down_event],
    )
    # *********** 添加中间件 *********** #

    # 跨域中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    # *********** 异常处理 *********** #

    # http 异常处理
    app.add_exception_handler(HTTPException, handler=handle_http_exception)
    app.add_exception_handler(RequestValidationError, handle_request_exception)

    # *********** 路由导入 *********** #
    app.include_router(router=router, prefix="")

    # 正式环境 不显示api文档
    if not settings.DEBUG:
        app.docs_url = None
        app.redoc_url = None
        app.openapi_url = None

    return app
