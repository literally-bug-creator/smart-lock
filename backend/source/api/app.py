"""API of Backend."""

from api.access import router as access_router
from api.users import router as users_router
from fastapi import FastAPI

app = FastAPI(title='SmartLock Backend API')

app.include_router(users_router)
app.include_router(access_router)
