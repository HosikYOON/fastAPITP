from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.db.database import get_db
from app.core.security import decode_access_token
from app.repositories import user as user_repository
from app.db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = await user_repository.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for login and user creation endpoints
        if request.url.path in ["/users/token", "/users/"] and request.method == "POST":
            response = await call_next(request)
            return response

        # For other endpoints, try to authenticate
        try:
            # This is a simplified example. In a real app, you'd extract the token
            # from headers and validate it here.
            # For now, we'll just let the get_current_user dependency handle it
            # when it's called by the router.
            response = await call_next(request)
            return response
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})