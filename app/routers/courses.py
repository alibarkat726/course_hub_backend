from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db_session
from ..dependencies import get_tenant_id, get_current_user, require_roles
from ..models import Course
from ..schemas import CourseCreate, CourseRead


router = APIRouter(prefix="/courses", tags=["courses"])

DbDep = Annotated[AsyncSession, Depends(get_db_session)]
TenantDep = Annotated[str, Depends(get_tenant_id)]


@router.get("/", response_model=List[CourseRead])
async def list_courses(db: DbDep, tenant_id: TenantDep):
    stmt = select(Course).where(Course.tenant_id == int(tenant_id)) if tenant_id else select(Course)
    result = await db.execute(stmt)
    return list(result.scalars())


@router.post("/", response_model=CourseRead, dependencies=[Depends(require_roles("admin", "instructor"))])
async def create_course(
    data: CourseCreate,
    db: DbDep,
    tenant_id: TenantDep,
    current_user=Depends(get_current_user),
):
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing tenant header")
    if int(tenant_id) != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cross-tenant access denied")
    course = Course(
        title=data.title,
        description=data.description,
        instructor_id=data.instructor_id,
        tenant_id=int(tenant_id),
        currency=data.currency,
        price_cents= data.price_cents *100 if data.price_cents else 0
    )
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course


