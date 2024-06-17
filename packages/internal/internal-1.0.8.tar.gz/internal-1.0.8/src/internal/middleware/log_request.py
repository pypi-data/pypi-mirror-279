import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware


class LogRequestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.app = app

    async def dispatch(self, request: Request, call_next):
        # 记录请求的URL和参数
        url = request.url.path
        params = dict(request.query_params)
        body = await request.body()
        self.app.state.logger.info(f"URL: {url} - Params: {params} - Body: {body}")

        # 记录请求处理时间
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        self.app.state.logger.info(f"Completed in {process_time:.4f} seconds")
        return response
