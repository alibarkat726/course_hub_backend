from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="SET NULL"), nullable=True, index=True)

    provider: Mapped[str] = mapped_column(String(50), default="stripe")
    provider_payment_id: Mapped[str] = mapped_column(String(200), unique=True)
    amount_cents: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(10), default="usd")
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, paid, failed, refunded

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
