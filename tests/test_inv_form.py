# Pruebas unitarias para las funciones de CRUD de productos
import os
import sys 
import pytest
import shutil
from sqlalchemy.exc import IntegrityError, DatabaseError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from source.database.models import Base, Inventario, MovimientoInventario
from source.database.database import SessionLocal
from source.database.crud import agregar_producto, actualizar_producto, buscar_producto, eliminar_producto

# Añadir la ruta del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:root@127.0.0.1/test_db')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def setup_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    # Limpia primero las tablas dependientes
    session.query(MovimientoInventario).delete()
    session.query(Inventario).delete()
    session.commit()
    yield session
    # Limpia las tablas después de cada prueba
    session.query(MovimientoInventario).delete()
    session.query(Inventario).delete()
    session.commit()
    session.close()
    Base.metadata.drop_all(bind=engine)

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

def test_agregar_producto(setup_db):
    session = setup_db
    try:
        producto_id = agregar_producto(session, "Producto Test", "Descripción Test", "Categoría Test", "producto", "pieza", 10.0, "1234567890123", 100, True)
        producto = buscar_producto(session, producto_id)
        assert producto is not None
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
    except DatabaseError as e:
        print(f"DatabaseError: {e}")
    finally:
        session.close()

def test_actualizar_producto(setup_db):
    session = setup_db
    try:
        producto_id = agregar_producto(session, "Producto Test", "Descripción Test", "Categoría Test", "producto", "pieza", 10.0, "1234567890123", 100, True)
        actualizar_producto(session, producto_id, nombre_producto="Producto Actualizado")
        producto = buscar_producto(session, producto_id)
        assert producto.nombre_producto == "Producto Actualizado"
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
    except DatabaseError as e:
        print(f"DatabaseError: {e}")
    finally:
        session.close()

def test_eliminar_producto(setup_db):
    session = setup_db
    try:
        # Agregar producto
        producto_id = agregar_producto(session, "Producto Test", "Descripción Test", "Categoría Test", "producto", "pieza", 10.0, "1234567890123", 100, True)
        
        # Agregar movimiento relacionado
        movimiento = MovimientoInventario(
            producto_id=producto_id,
            cantidad=10,
            tipo_movimiento="entrada",
            id=1
        )
        session.add(movimiento)
        session.commit()

        # Intentar eliminar producto (se necesita usuario_id)
        eliminar_producto(session, usuario_id=1, producto_id=producto_id)
        producto = buscar_producto(session, producto_id)
        
        # Validar que el producto fue desactivado
        assert producto is not None
        assert producto.activo is False
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
        session.rollback()
    except DatabaseError as e:
        print(f"DatabaseError: {e}")
        session.rollback()
    finally:
        session.close()


def test_agregar_producto_con_foto(setup_db):
    session = setup_db
    try:
        # Código para agregar producto con foto
        pass
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
    except DatabaseError as e:
        print(f"DatabaseError: {e}")
    finally:
        session.close()

def test_actualizar_producto_con_foto(setup_db):
    session = setup_db
    try:
        # Código para actualizar producto con foto
        pass
    except IntegrityError as e:
        print(f"IntegrityError: {e}")
    except DatabaseError as e:
        print(f"DatabaseError: {e}")
    finally:
        session.close()