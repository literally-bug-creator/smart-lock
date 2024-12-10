from fastapi import FastAPI

from api.access import router as access_router
from api.users import router as users_router

app = FastAPI(title='SmartLock Backend API')

app.include_router(users_router)
app.include_router(access_router)
