from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from functools import wraps
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Allow access to login and register pages without authentication
        if request.url.path in ['/artgalleryproject/auth/login', '/artgalleryproject/auth/register']:
            return await call_next(request)
            
        if not request.cookies.get('session'):
            if request.url.path.startswith('/artgalleryproject/api/'):
                raise HTTPException(status_code=401, detail="Not authenticated")
            return RedirectResponse(url="/artgalleryproject/auth/login", status_code=303)
        return await call_next(request)

def login_required(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        # Allow access to login and register pages without authentication
        if request.url.path in ['/artgalleryproject/auth/login', '/artgalleryproject/auth/register']:
            return await func(request, *args, **kwargs)
            
        if not request.cookies.get('session'):
            if request.url.path.startswith('/artgalleryproject/api/'):
                raise HTTPException(status_code=401, detail="Not authenticated")
            return RedirectResponse(url="/artgalleryproject/auth/login", status_code=303)
        return await func(request, *args, **kwargs)
    return wrapper 