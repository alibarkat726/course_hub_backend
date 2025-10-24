from typing import Annotated
import jwt

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from ..database import get_db_session
from ..models import User
from ..utils import create_access_token, create_refresh_token,verify_password
from ..dependencies import get_current_user
from ..models import Organization



router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    role: str = "student"
    tenant_id: int


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

DbDep = Annotated[AsyncSession, Depends(get_db_session)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterRequest, db: DbDep):
    # check existing email
    print("password without hash: ", data.password)
    existing = await db.scalar(select(User).where(User.email == data.email))
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    # validate tenant
    org = await db.scalar(select(Organization).where(Organization.id == data.tenant_id))
    if not org:
        raise HTTPException(status_code=400, detail="Invalid tenant ID")
    
    # create user
    user = User(
        email=data.email,
        full_name=f"{data.firstName} {data.lastName}",
        role=data.role,
        hashed_password=pwd_context.hash(data.password),
        tenant_id=data.tenant_id,
)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: DbDep):
    user = await db.scalar(select(User).where(User.email == data.email))
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


# OAuth2 password grant-compatible token endpoint
@router.post("/token", response_model=TokenResponse)
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbDep = None):
    # OAuth2 form expects username/password fields
    user = await db.scalar(select(User).where(User.email == form_data.username))
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshRequest):
    # For simplicity, accept refresh token and mint a new access token for same subject
    try:
        payload = jwt.decode(data.refresh_token, options={"verify_signature": False})
        sub = payload.get("sub")
        if not sub:
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return TokenResponse(
        access_token=create_access_token(str(sub)),
        refresh_token=data.refresh_token,
    )


class MeResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    tenant_id: int


@router.get("/me", response_model=MeResponse)
async def me(current_user: Annotated[User, Depends(get_current_user)]):
    return MeResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        tenant_id=current_user.tenant_id,
    )


@router.get("/user/profile", response_model=MeResponse)
async def get_user_profile(current_user: Annotated[User, Depends(get_current_user)]):
    """Get detailed user profile information"""
    return MeResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        tenant_id=current_user.tenant_id,
    )


