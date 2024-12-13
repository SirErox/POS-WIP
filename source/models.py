from sqlalchemy import Column,Integer,String,Enum
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Table_usuario(Base):
    __tablename__='usuarios'
    id=Column(Integer,primary_key=True)
    nombre=Column(String(50))
    username=Column(String(50),unique=True)
    password=Column(String(255))
    rol=Column(Enum('administrador','cajero'),default='cajero')