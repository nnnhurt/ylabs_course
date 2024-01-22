from pydantic import BaseModel
from uuid import UUID


class CreateDish(BaseModel):
    title: str
    description: str
    price: float


class Dish(CreateDish):
    class Config:
        orm_mode = True
    id: UUID


class CreateSubmenu(BaseModel):
    title: str
    description: str


class Submenu(CreateSubmenu):
    class Config:
        orm_mode = True
    id: UUID
    dishes_count: int


class CreateMenu(BaseModel):
    title: str
    description: str


class Menu(CreateMenu):
    id: UUID
    submenus_count: int
    dishes_count: int
