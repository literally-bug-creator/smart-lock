from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/identify")
async def identify(file: UploadFile = File(...)):
    return JSONResponse(content={"message": "Success"}, status_code=200)
