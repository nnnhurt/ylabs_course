from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, schemas
from sql_app.database import get_db

router = APIRouter()


@router.get("/menus/{menu_id}", response_model=schemas.Menu)
def read_menu(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="menu not found")
    db_menu.submenus_count = crud.submenu_count(db, menu_id=menu_id)
    db_menu.dishes_count = crud.dish_count(db, menu_id=menu_id)
    return db_menu


@router.get("/menus", response_model=list[schemas.Menu])
def read_all_menus(db: Session = Depends(get_db)):
    menus = crud.get_all_menu(db)
    for row in menus:
        row.submenu_count = crud.submenu_count_in_menu(db, menu_id=row.id)
        row.dishes_count = crud.dish_count_in_menu(db, menu_id=row.id)
        return menus


@router.post("/menus", response_model=schemas.Menu, status_code=HTTPStatus.CREATED)
def create_menu(menu: schemas.CreateMenu, db: Session = Depends(get_db)):
    db_menu = crud.create_menu(db=db, menu=menu)
    db_menu.submenu_count = (
        crud.submenu_count_in_menu(db, menu_id=db_menu.id)
    )
    db_menu.dish_count = crud.dish_count_in_menu(db, menu_id=db_menu.id)
    return db_menu


@router.patch("/menus/{menu_id}", response_model=schemas.Menu)
def update_menu(menu_id: UUID, menu: schemas.Menu, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(
            status_code=HTTPException.NOT_FOUND, detail="menu not found")
    db_menu = crud.update_menu(db=db, menu_id=menu_id, menu=menu)
    db_menu.submenu_count = (crud.submenu_count_in_menu(db, menu_id=menu_id))
    db_menu.dish_count = crud.dish_count_in_menu(db, menu_id=menu_id)
    return db_menu


@router.delete("/menus/{menu_id}")
def delete_menu(menu_id: UUID, db: Session = Depends(get_db)):
    crud.delete_menu(db=db, menu_id=menu_id)
    return {'status': True, 'message': 'The menu has been deleted'}
