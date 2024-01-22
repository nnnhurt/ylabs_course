from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sql_app.database import Base
import uuid


class Dish(Base):
    __tablename__ = 'dish'
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4)
    title = Column(String(100), index=True)
    description = Column(String(255), index=True)
    price = Column(Float(decimal_return_scale=2), index=True)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey(
        'submenu.id', ondelete="cascade"))


class Submenu(Base):
    __tablename__ = 'submenu'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), index=True)
    description = Column(String(255), index=True)
    menu_id = Column(UUID(as_uuid=True), ForeignKey(
        'menu.id', ondelete="cascade"))


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), index=True)
    description = Column(String(255), index=True)
