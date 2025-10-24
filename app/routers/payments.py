from typing import Annotated

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_db_session
from ..dependencies import get_current_user, get_tenant_id, require_roles
from ..models import Course, Payment, User
from ..schemas import PaymentCreate, PaymentRead


router = APIRouter(prefix="/payments", tags=["payments"])

DbDep = Annotated[AsyncSession, Depends(get_db_session)]


@router.post("/checkout", response_model=dict)
async def create_checkout_session(
    payload: PaymentCreate,
    db: DbDep,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[User, Depends(get_current_user)],
):
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Missing tenant header")
    if user.tenant_id != int(tenant_id):
        raise HTTPException(status_code=403, detail="Cross-tenant access denied")

    course = await db.scalar(select(Course).where(Course.id == payload.course_id, Course.tenant_id == int(tenant_id)))
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.price_cents <= 0:
        raise HTTPException(status_code=400, detail="Course not purchasable")

    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": course.currency,
                    "product_data": {"name": course.title},
                    "unit_amount": course.price_cents,
                },
                "quantity": 1,
            }
        ],
        metadata={
            "tenant_id": str(tenant_id),
            "user_id": str(user.id),
            "course_id": str(course.id),
        },
        success_url="http://localhost:3000/payments/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:3000/payments/cancel",
    )

    payment = Payment(
        tenant_id=int(tenant_id),
        user_id=user.id,
        course_id=course.id,
        provider="stripe",
        provider_payment_id=session.id,
        amount_cents=course.price_cents,
        currency=course.currency,
        status="pending",
    )
    db.add(payment)
    await db.commit()
    return {"checkout_url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: DbDep):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Stripe webhook not configured")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        provider_payment_id = session["id"]
        payment = await db.scalar(select(Payment).where(Payment.provider_payment_id == provider_payment_id))
        if payment:
            payment.status = "paid"
            await db.commit()
    return {"received": True}


@router.get("/mine", response_model=list[PaymentRead])
async def list_my_payments(
    db: DbDep,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[User, Depends(get_current_user)],
):
    if not tenant_id or user.tenant_id != int(tenant_id):
        raise HTTPException(status_code=403, detail="Cross-tenant access denied")
    result = await db.execute(
        select(Payment).where(Payment.tenant_id == int(tenant_id), Payment.user_id == user.id).order_by(Payment.id.desc())
    )
    return list(result.scalars())


@router.get("/", response_model=list[PaymentRead], dependencies=[Depends(require_roles("admin", "instructor"))])
async def list_tenant_payments(
    db: DbDep,
    tenant_id: Annotated[str, Depends(get_tenant_id)],
    user: Annotated[User, Depends(get_current_user)],
):
    if not tenant_id or user.tenant_id != int(tenant_id):
        raise HTTPException(status_code=403, detail="Cross-tenant access denied")
    result = await db.execute(
        select(Payment).where(Payment.tenant_id == int(tenant_id)).order_by(Payment.id.desc())
    )
    return list(result.scalars())


