from sqlalchemy import (Column, ForeignKey, Integer, String, Date, TIMESTAMP, func, event,
                        Boolean, DateTime, Enum, DECIMAL, Text)
from datetime import datetime
from source.database.database import Base
from source.Utils.helpers import calcular_edad, calcular_antiguedad 
from sqlalchemy.orm import relationship

class Table_usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    nombre_completo = Column(String(100), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    edad = Column(Integer, nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    antiguedad = Column(Integer, nullable=True)
    curp = Column(String(18), nullable=True)
    rol = Column(String(50), nullable=True)
    estado = Column(String(50), nullable=True)
    foto_perfil = Column(String(255), nullable=True)
    ultimo_editor = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, server_default=func.now(), onupdate=func.now())

    auditorias = relationship("Auditoria", order_by="Auditoria.id", back_populates="usuario")

@event.listens_for(Table_usuario, 'before_insert')
@event.listens_for(Table_usuario, 'before_update')
def calcular_datos_automaticos(target):
    """Calcula la edad y antigüedad antes de guardar en la base de datos."""
    if target.fecha_nacimiento:
        target.edad = calcular_edad(target.fecha_nacimiento)
    if target.fecha_inicio:
        target.antiguedad = calcular_antiguedad(target.fecha_inicio)

class Inventario(Base):
    __tablename__ = 'inventario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_producto = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(100), nullable=True)
    tipo = Column(Enum('producto', 'servicio'), nullable=False, default='producto')
    unidad_medida = Column(String(50), default='pieza')
    cantidad_stock = Column(Integer, default=0)
    precio = Column(DECIMAL(10, 2), nullable=False)
    codigo_barras = Column(String(100), unique=True)
    foto = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Inventario(nombre_producto={self.nombre_producto}, categoria={self.categoria})>"

class MovimientoInventario(Base):
    __tablename__ = 'movimientos_inventario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey('inventario.id'), nullable=False)
    tipo_movimiento = Column(String(50), nullable=False)  # 'entrada' o 'salida'
    cantidad = Column(Integer, nullable=False)
    fecha_movimiento = Column(DateTime, server_default=func.now())
    descripcion = Column(String(255), nullable=True)

    producto = relationship("Inventario", back_populates="movimientos")

Inventario.movimientos = relationship("MovimientoInventario", order_by=MovimientoInventario.id, back_populates="producto")

class Auditoria(Base):
    __tablename__ = 'auditoria'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    accion = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=True)
    fecha = Column(DateTime, default=datetime.now)

    usuario = relationship("Table_usuario", back_populates="auditorias")

Table_usuario.auditorias = relationship("Auditoria", order_by=Auditoria.id, back_populates="usuario")

class Ventas(Base):
    __tablename__ = 'ventas'

    id=Column(Integer, primary_key=True, autoincrement=True)
    fecha=Column(DateTime,default=datetime.now,nullable=True)
    total=Column(DECIMAL(10, 2), nullable=False)
    metodo_pago=Column(Enum('efectivo', 'tarjeta', 'Mixto'), nullable=False)
    cambio=Column(DECIMAL(10, 2), nullable=False,default=0.0)
    usuario_id=Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    recibo_generado=Column(Enum('Digital','Impreso','Ninguno'), nullable=True,default='Ninguno')
    estado=Column(Enum('Completada','Cancelada'), nullable=True,default='Completada')

    detalles=relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'

    id=Column(Integer, primary_key=True, autoincrement=True)
    venta_id=Column(Integer, ForeignKey('ventas.id'), nullable=False)
    producto_id=Column(Integer, ForeignKey('inventario.id'), nullable=False)
    cantidad=Column(Integer, nullable=False)
    precio_unitario=Column(DECIMAL(10, 2), nullable=False)
    subtotal=Column(DECIMAL(10, 2), nullable=False)
    descuento=Column(DECIMAL(10, 2), nullable=False,default=0.0)

    venta=relationship("Ventas", back_populates="detalles")