from sqlalchemy import func
from sqlalchemy.orm import Session


from sql_app import models, schemas


def get_dish(db: Session, submenu_id: int, dish_id: int):
    db_dish = (
        db.query(models.Dish)
        .filter(models.Dish.submenu_id == submenu_id)
        .filter(models.Dish.id == dish_id).first()
    )
    if db_dish is not None:
        db_dish.price = str(db_dish.price)
    return db_dish


def get_all_dish(db: Session, submenu_id: int):
    db_dishes = db.query(models.Dish).filter(
        models.Dish.submenu_id == submenu_id).all()
    for dish in db_dishes:
        dish.price = str(dish.price)
    return db_dishes


def create_dish(db: Session, dish: schemas.CreateDish, submenu_id: int):
    new_dish = models.Dish(**dish.model_dump())
    new_dish.submenu_id = submenu_id
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    new_dish.price = str(new_dish.price)
    return new_dish


def update_dish(db: Session, dish_id: int, dish: schemas.CreateDish, submenu_id: int):
    db_dish = get_dish(db, submenu_id, dish_id)
    db_dish.title = dish.title
    db_dish.description = dish.description
    db_dish.price = dish.price
    db.commit()
    db.refresh(db_dish)
    if db_dish is not None:
        db_dish.price = str(db_dish.price)
    return db_dish


def delete_dish(db: Session, dish_id: int, submenu_id: int):
    db_dish = get_dish(db, submenu_id, dish_id)
    db.delete(db_dish)
    db.commit()


def dish_count_in_menu(db: Session, menu_id: int):
    return (db.query(func.count(models.Dish.id)).join(models.Submenu).join(models.Menu).filter(models.Menu.id == menu_id).scalar())


def dish_count_in_submenu(db: Session, submenu_id: int):
    return (
        db.query(models.Dish)
        .filter(models.Dish.submenu_id == submenu_id)
        .count()
    )


def get_submenu(db: Session, menu_id: int, submenu_id: int):
    return (db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).filter(models.Submenu.id == submenu_id).first())


def get_all_submenu(db: Session, menu_id: int):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()


def create_submenu(db: Session, menu_id: int, submenu: schemas.CreateSubmenu):
    db_submenu = models.Submenu(**submenu.model_dump())
    db_submenu.menu_id = menu_id
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def update_submenu(db: Session, menu_id: int, submenu_id: int, submenu: schemas.Submenu):
    db_submenu = get_submenu(db, menu_id, submenu_id)
    db_submenu.title = submenu.title
    db_submenu.description = submenu.description
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def delete_submenu(db: Session, menu_id: int, submenu_id: int):
    db_submenu = get_submenu(db, menu_id, submenu_id)
    db.delete(db_submenu)
    db.commit()


def submenu_count_in_menu(db: Session, menu_id: int):
    return (db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).count())


def get_menu(db: Session, menu_id: int):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def get_all_menu(db: Session):
    return db.query(models.Menu).all()


def create_menu(db: Session, menu: schemas.CreateMenu):
    new_menu = models.Menu(**menu.model_dump())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


def update_menu(db: Session, menu_id: int, menu: schemas.Menu):
    db_menu = get_menu(db, menu_id)
    db_menu.title = menu.title
    db_menu.description = menu.description
    db.commit()
    db.refresh(db_menu)
    return db_menu


def delete_menu(db: Session, menu_id: int):
    db_menu = get_menu(db, menu_id)
    db.delete(db_menu)
    db.commit()
