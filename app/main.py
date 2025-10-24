from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import auth_router, orgs_router, courses_router, payments_router
from .database import engine, Base
from .middleware import TenantMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title="CourseHub", version="0.1.0")

   
    app.add_middleware(TenantMiddleware)

    # Add CORS middleware 
    origins = [
        "http://localhost:3000",    # Flutter web (if running on localhost)
        "http://127.0.0.1:3000",
        "http://localhost:8080",    # Some Flutter web servers use 8080
        "http://127.0.0.1:8080",
        "https://your-production-domain.com",  # For deployment
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # or ["http://localhost:3000", "http://127.0.0.1:3000"]
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check route
    @app.get("/health")
    def health_check():
        return {"status": "ok", "env": settings.ENVIRONMENT}

    # Database startup event (create tables)
    @app.on_event("startup")
    async def on_startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Include all routers
    app.include_router(auth_router)
    app.include_router(orgs_router)
    app.include_router(courses_router)
    app.include_router(payments_router)

    return app


app = create_app()
