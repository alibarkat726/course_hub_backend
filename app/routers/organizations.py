from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db_session
from ..models import Organization
from ..schemas import OrganizationCreate, OrganizationRead


router = APIRouter(prefix="/organizations", tags=["organizations"])

DbDep = Annotated[AsyncSession, Depends(get_db_session)]


@router.post("/", response_model=OrganizationRead)
async def create_org(data: OrganizationCreate, db: DbDep):
    existing = await db.scalar(select(Organization).where((Organization.name == data.name) | (Organization.slug == data.slug)))
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization already exists")
    org = Organization(name=data.name, slug=data.slug)
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return org


@router.get("/{slug}", response_model=OrganizationRead)
async def get_org(slug: str, db: DbDep):
    org = await db.scalar(select(Organization).where(Organization.slug == slug))
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return org


