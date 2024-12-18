import pytest
import os
import shutil
from source.database.database import SessionLocal
from source.database.crud import agregar_producto, actualizar_producto, buscar_producto
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

@pytest.fixture
def setup_fotos():
    # Crear el directorio de fotos de prueba
    os.makedirs('test_fotos', exist_ok=True)
    yield
    # Eliminar el directorio de fotos de prueba después de las pruebas
    shutil.rmtree('test_fotos')

def test_agregar_producto_con_foto(session, setup_fotos):
    foto_path = 'test_fotos/test_image.jpg'
    with open(foto_path, 'w') as f:
        f.write('test image content')

    producto_id = agregar_producto(
        session,
        "Producto Test",
        "Descripción Test",
        "Categoría Test",
        "producto",
        "pieza",
        10.0,
        "1234567890123",
        100,
        True,
        foto_path
    )
    producto = buscar_producto(session, producto_id)
    assert producto is not None
    assert producto.nombre_producto == "Producto Test"
    assert producto.foto == 'fotos/Producto Test_item.jpg'
    assert os.path.exists(producto.foto)

def test_actualizar_producto_con_foto(session, setup_fotos):
    foto_path = 'test_fotos/test_image.jpg'
    with open(foto_path, 'w') as f:
        f.write('test image content')

    producto_id = agregar_producto(
        session,
        "Producto Test",
        "Descripción Test",
        "Categoría Test",
        "producto",
        "pieza",
        10.0,
        "1234567890123",
        100,
        True,
        foto_path
    )

    nueva_foto_path = 'test_fotos/test_image_updated.jpg'
    with open(nueva_foto_path, 'w') as f:
        f.write('test image updated content')

    actualizar_producto(
        session,
        producto_id,
        nombre_producto="Producto Actualizado",
        descripcion="Descripción Actualizada",
        categoria="Categoría Actualizada",
        tipo="producto",
        unidad_medida="pieza",
        precio=20.0,
        codigo_barras="9876543210987",
        cantidad_stock=200,
        activo=True,
        foto=nueva_foto_path
    )
    producto = buscar_producto(session, producto_id)
    assert producto is not None
    assert producto.nombre_producto == "Producto Actualizado"
    assert producto.foto == 'fotos/Producto Actualizado_item.jpg'
    assert os.path.exists(producto.foto)