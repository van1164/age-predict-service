from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_photo(file: UploadFile):
    return {"age":1 }