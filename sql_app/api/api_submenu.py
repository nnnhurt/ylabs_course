from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, schemas
from sql_app.database import get_db

router = APIRouter()


@router.get("/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.Submenu)
def read_submenu(menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="submenu not found")
    db_submenu.dishes_count = crud.dish_count_in_submenu(
        db, submenu_id=db_submenu.id)
    return db_submenu


@router.get("/menus/{menu_id}/submenus", response_model=list[schemas.Submenu])
def read_all_submenus(menu_id: UUID, db: Session = Depends(get_db)):
    submenus = crud.get_all_submenu(db, menu_id=menu_id)
    for row in submenus:
        row.dishes_count = crud.dish_count_in_submenu(db, submenu_id=row.id)
    return submenus


@router.post("/menus/{menu_id}/submenus", response_model=schemas.Submenu, status_code=HTTPStatus.CREATED)
def create_submenu(menu_id: UUID, submenu: schemas.CreateSubmenu, db: Session = Depends(get_db)):
    db_submenu = crud.create_submenu(db, menu_id=menu_id, submenu=submenu)
    db_submenu.dishes_count = crud.dish_count_in_submenu(
        db, submenu_id=db_submenu.id)
    return db_submenu


@router.patch("/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.Submenu)
def update_submenu(menu_id: UUID, submenu_id: UUID, submenu: schemas.CreateSubmenu, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='submenu not found')
    db_submenu = crud.update_submenu(
        db, menu_id=menu_id, submenu_id=submenu_id, submenu=submenu)
    db_submenu.dishes_count = crud.dish_count_in_submenu(
        db, submenu_id=db_submenu.id)
    return db_submenu


@router.delete("/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    crud.delete_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    return {'status': True, 'message': 'The submenu has been deleted'}
