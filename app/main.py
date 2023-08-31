from fastapi import FastAPI
from .routers import posts, users,auth
from . import models
from .database import engine
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"message": "Root"}

