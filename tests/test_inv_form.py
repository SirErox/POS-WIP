import pytest
import os, sys
# Añadir la ruta del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from source.database.database import SessionLocal
from source.database.models import Inventario 
@pytest.fixture
def setup_db():
    session = SessionLocal()
    # Limpia los datos antes de cada prueba
    session.query(Inventario).delete()
    session.commit()
    yield session
    # Limpia los datos después de cada prueba
    session.query(Inventario).delete()
    session.commit()
    session.close()
"""
def test_actualizar_producto(setup_db):
    session = setup_db

    # Crear un producto de prueba
    producto = Inventario(
        nombre_producto="Prueba",
        descripcion="Producto de prueba",
        categoria="General",
        tipo="producto",
        unidad_medida="pieza",
        cantidad_stock=10,
        precio=100.0,
        codigo_barras="123456789012",
        activo=1
    )
    session.add(producto)
    session.commit()

    # Actualizar el producto
    producto.precio = 120.0
    session.commit()

    # Verificar que el cambio se haya aplicado
    producto_actualizado = session.query(Inventario).filter_by(id=producto.id).first()
    assert producto_actualizado.precio == 120.0
"""
def test_eliminar_producto(setup_db):
    session = setup_db

    # Crear un producto de prueba
    producto = Inventario(
        nombre_producto="Eliminar",
        descripcion="Producto para eliminar",
        categoria="General",
        tipo="producto",
        unidad_medida="pieza",
        cantidad_stock=5,
        precio=50.0,
        codigo_barras="987654321098",
        activo=1
    )
    session.add(producto)
    session.commit()

    # Eliminar el producto
    session.delete(producto)
    session.commit()

    # Verificar que el producto no exista
    producto_eliminado = session.query(Inventario).filter_by(id=producto.id).first()
    assert producto_eliminado is None