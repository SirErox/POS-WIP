import pytest
from source.database.database import SessionLocal
from source.database.crud import agregar_producto, buscar_producto
from source.database.models import Inventario

@pytest.fixture
def session():
    session = SessionLocal()
    # Limpia los datos antes de cada prueba
    session.query(Inventario).delete()
    session.commit()
    yield session
    # Limpia los datos después de cada prueba
    session.query(Inventario).delete()
    session.commit()
    session.close()

def test_agregar_producto(session):
    producto_id = agregar_producto(session, "Producto Test", "Descripción Test", "Categoría Test", "producto", "pieza", 10.0, "1234567890123", 100, True)
    producto = buscar_producto(session, producto_id)
    assert producto is not None
    assert producto.nombre_producto == "Producto Test"
    assert producto.descripcion == "Descripción Test"
    assert producto.categoria == "Categoría Test"
    assert producto.tipo == "producto"
    assert producto.unidad_medida == "pieza"
    assert producto.precio == 10.0
    assert producto.codigo_barras == "1234567890123"
    assert producto.cantidad_stock == 100
    assert producto.activo is True

def test_buscar_producto(session):
    producto_id = agregar_producto(session, "Producto Test", "Descripción Test", "Categoría Test", "producto", "pieza", 10.0, "1234567890123", 100, True)
    producto = buscar_producto(session, producto_id)
    assert producto is not None
    assert producto.nombre_producto == "Producto Test"