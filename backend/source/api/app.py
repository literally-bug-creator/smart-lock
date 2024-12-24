"""API of Backend."""

from api.users import router as users_router
from api.access import router as access_router
from api.employee import router as employee_router
from fastapi import FastAPI

app = FastAPI(title='SmartLock Backend API')

app.include_router(users_router)
app.include_router(access_router)
app.include_router(employee_router)
