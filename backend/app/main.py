
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.lifespan import app_lifespan


# ==========================================
# APPLICATION INITIALIZATION
# ==========================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "KhyathiAI - An extensible AI-powered platform."
    ),
    lifespan=app_lifespan,
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# API ROUTE REGISTRATION
# ==========================================

app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)
