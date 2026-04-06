from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.orders import router as orders_router

import app.models.__all_models # noqa

from app.core.config import settings
from app.api.products import router as products_router

app = FastAPI(
    title="Limpeza Store API",
    version="0.1.0"
)

app.include_router(products_router)
app.include_router(orders_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "env": settings.ENV
    }