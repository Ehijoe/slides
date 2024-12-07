from fastapi import FastAPI

from backend.src.auth.router import router as auth_router
from backend.src.slides.router import router as slides_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world!"}

app.include_router(auth_router, prefix="/auth")
app.include_router(slides_router, prefix="/slides")
