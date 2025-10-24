from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from ..config import settings


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        header_name = settings.TENANT_HEADER
        tenant_id = request.headers.get(header_name)
        request.state.tenant_id = tenant_id or ""
        response: Response = await call_next(request)
        return response


