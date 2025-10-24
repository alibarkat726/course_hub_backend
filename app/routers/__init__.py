from .auth import router as auth_router
from .organizations import router as orgs_router
from .courses import router as courses_router
from .payments import router as payments_router

__all__ = [
    "auth_router",
    "orgs_router",
    "courses_router",
    "payments_router",
]


