from api.users import router as users_router
from fastapi import FastAPI

app = FastAPI(title="SmartLock API")

app.include_router(users_router)
