from fastapi import FastAPI

from sql_app import models
from sql_app.api import api_menu, api_submenu, api_dish
from sql_app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_prefix="/api/v1")
app.include_router(api_menu.router)
app.include_router(api_submenu.router)
app.include_router(api_dish.router)
