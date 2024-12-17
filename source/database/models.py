from sqlalchemy import (Column, Integer, String, Date, TIMESTAMP, func, event,
                        Float,Boolean,DateTime)
from datetime import datetime
from source.database.database import Base
from source.Utils.helpers import calcular_edad,calcular_antiguedad

class Table_usuario(Base):
    __tablename__='usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nombre_completo = Column(String(255), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    edad = Column(Integer, nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    antiguedad = Column(Integer, nullable=True)
    curp = Column(String(20), nullable=True)
    rol = Column(String(50), nullable=False)
    estado = Column(String(10), default="Activo")  # Activo/Inactivo
    foto_perfil = Column(String(255), nullable=True)
    ultimo_editor = Column(String(50), nullable=True)  # Usuario que editó
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
class Inventario(Base):
    __tablename__ = 'inventario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)  # 'Producto' o 'Servicio'
    stock = Column(Integer, nullable=True)  # NULL para servicios
    unidad = Column(String(20), nullable=True)  # Unidad de medida
    codigo_barras = Column(String(50), nullable=True)
    precio = Column(Float, nullable=False)
    costo = Column(Float, nullable=True)  # Costo del producto
    proveedor = Column(String(100), nullable=True)
    descripcion = Column(String(255), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activo = Column(Boolean, default=True)  # Estado activo/inactivo

    def __repr__(self):
        return (f"<Inventario(id={self.id}, nombre={self.nombre}, tipo={self.tipo}, "
                f"stock={self.stock}, precio={self.precio}, costo={self.costo}, "
                f"proveedor={self.proveedor}, activo={self.activo})>")


# Event Listener para calcular edad y antigüedad automáticamente
@event.listens_for(Table_usuario, 'before_insert')
@event.listens_for(Table_usuario, 'before_update')
def calcular_datos_automaticos(mapper, connection, target):
    """Calcula la edad y antigüedad antes de guardar en la base de datos."""
    if target.fecha_nacimiento:
        target.edad = calcular_edad(target.fecha_nacimiento)
    if target.fecha_inicio:
        target.antiguedad = calcular_antiguedad(target.fecha_inicio)
