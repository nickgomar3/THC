from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.router import api_router
from core.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Shutdown
    await engine.dispose()
    

app = FastAPI(lifespan=lifespan)


app.include_router(api_router)


@app.get("/")
def home():
    return {"message": "Welcome to the Home Page"}
