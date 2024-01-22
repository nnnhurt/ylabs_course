from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, schemas
from sql_app.database import get_db

router = APIRouter()


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def read_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, submenu_id=submenu_id, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="dish not found")
    return db_dish


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[schemas.Dish])
def read_all_dishes(submenu_id: UUID, db: Session = Depends(get_db)):
    dishes = crud.get_all_dish(db, submenu_id=submenu_id)
    return dishes


@router.post("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=schemas.Dish, status_code=HTTPStatus.CREATED)
def create_dish(menu_id: UUID, submenu_id: UUID, dish: schemas.CreateDish, db: Session = Depends(get_db)):
    db_dish = crud.create_dish(
        db, submenu_id=submenu_id, dish=dish)
    return db_dish


@router.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def update_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dish: schemas.CreateDish, db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, submenu_id=submenu_id, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="dish not found")
    db_dish = crud.update_dish(
        db, submenu_id=submenu_id, dish_id=dish_id, dish=dish)
    return db_dish


@router.delete("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
    crud.delete_dish(db, submenu_id=submenu_id, dish_id=dish_id)
    return {'status': True, 'message': 'The dish has been deleted'}
