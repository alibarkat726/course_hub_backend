from pydantic import BaseModel


class PaymentCreate(BaseModel):
    course_id: int


class PaymentRead(BaseModel):
    id: int
    tenant_id: int
    user_id: int | None
    course_id: int | None
    amount_cents: int
    currency: str
    status: str
    provider: str
    provider_payment_id: str

    class Config:
        from_attributes = True


