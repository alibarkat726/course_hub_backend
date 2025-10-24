from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .config import settings
from .database import get_db_session
from .models import User


async def get_tenant_id(request: Request, x_tenant_id: str | None = Header(default=None, alias=None)) -> str:
    # Prefer middleware-injected tenant; fall back to header parameter
    tenant_from_state = getattr(request.state, "tenant_id", None)
    if tenant_from_state:
        return tenant_from_state
    if x_tenant_id:
        return x_tenant_id
    return ""


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


DbDep = Annotated[AsyncSession, Depends(get_db_session)]


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DbDep) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_roles(*allowed_roles: str):
    async def checker(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user

    return checker



