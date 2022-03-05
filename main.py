from fastapi import FastAPI
from routes.test import user
app = FastAPI()
app.include_router(user)