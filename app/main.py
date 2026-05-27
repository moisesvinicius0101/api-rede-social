

from fastapi import FastAPI
from app.routers import (auth, follows, posts, users)
from app import models



app = FastAPI(title="API Rede Social", description="API Rede Social Simples")


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(follows.router)

