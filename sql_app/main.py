from fastapi import FastAPI

from sql_app import models
from sql_app.api import api_menu
from sql_app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_prefix="/api/v1")
app.include_router(api_menu.router)
# app.include_router(submenu.router)
