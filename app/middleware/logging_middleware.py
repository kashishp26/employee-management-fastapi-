import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_logger")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = f"{process_time:.2f}ms"
        
        logger.info(
            f"Method: {request.method} | Path: {request.url.path} | "
            f"Status: {response.status_code} | Time: {formatted_process_time}"
        )
        return response