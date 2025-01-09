from api.access import router as access_router
from api.employee import router as employee_router
from api.employee_images import router as employee_image_router
from api.file import router as file_router
from fastapi import FastAPI


app = FastAPI(title='SmartLock Backend API')

app.include_router(access_router)
app.include_router(employee_router)
app.include_router(employee_image_router)
app.include_router(file_router)
