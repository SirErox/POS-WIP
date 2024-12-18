import pytest
import os, sys
# Añadir la ruta del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from source.database.database import SessionLocal
from source.database.crud import agregar_producto, actualizar_producto, buscar_producto, eliminar_producto

@pytest.fixture
def session():
    session = SessionLocal()
    yield session
    session.close()

def test_agregar_producto(session):
    producto_id = agregar_producto(session, "Producto Test", "Descripción Test", "Categoría Test", "producto", "pieza", 10.0, "1234567890123", 100, True)
    producto = buscar_producto(session, producto_id)
    assert producto is not None
    assert producto.nombre_producto == "Producto Test"

def test_actualizar_producto(session):
    producto_id = agregar_producto(session, "Producto Test", "Descripción Test", "Categoría Test", "producto", "pieza", 10.0, "1234567890123", 100, True)
    actualizar_producto(session, producto_id, nombre_producto="Producto Actualizado")
    producto = buscar_producto(session, producto_id)
    assert producto.nombre_producto == "Producto Actualizado"

def test_eliminar_producto(session):
    producto_id = agregar_producto(session, "Producto Test", "Descripción Test", "Categoría Test", "producto", "pieza", 10.0, "1234567890123", 100, True)
    eliminar_producto(session, producto_id)
    producto = buscar_producto(session, producto_id)
    assert producto is not None
    assert producto.activo is False