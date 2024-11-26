from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/identify")
async def identify():
    return JSONResponse(content={"message": "Success"}, status_code=200)
