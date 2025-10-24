from pydantic import BaseModel, EmailStr


class OrganizationBase(BaseModel):
    name: str
    slug: str


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationRead(OrganizationBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str


class UserCreate(UserBase):
    password: str
    tenant_id: int


class UserRead(UserBase):
    id: int
    tenant_id: int

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    title: str
    description: str
    currency: str = "usd"
    price_cents: int = 0


class CourseCreate(CourseBase):
    instructor_id: int | None = None


class CourseRead(CourseBase):
    id: int
    tenant_id: int
    is_published: bool

    class Config:
        from_attributes = True


