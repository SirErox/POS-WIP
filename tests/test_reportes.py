import pytest
import os
from source.database.database import SessionLocal
from source.database.models import Inventario, MovimientoInventario
from source.UI.reportes.inv_report import VentanaReportes
from PyQt5.QtWidgets import QApplication
import sys

@pytest.fixture
def session():
    session = SessionLocal()
    # Limpia los datos antes de cada prueba
    session.query(MovimientoInventario).delete()
    session.query(Inventario).delete()
    session.commit()
    yield session
    # Limpia los datos después de cada prueba
    session.query(MovimientoInventario).delete()
    session.query(Inventario).delete()
    session.commit()
    session.close()

@pytest.fixture
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

def test_generar_reporte_inventario_excel(session, app, qtbot):
    # Añadir datos de prueba
    producto = Inventario(
        nombre_producto="Producto Test",
        descripcion="Descripción Test",
        categoria="Categoría Test",
        tipo="producto",
        unidad_medida="pieza",
        precio=10.0,
        codigo_barras="1234567890123",
        cantidad_stock=100,
        activo=True
    )
    session.add(producto)
    session.commit()

    ventana = VentanaReportes()
    qtbot.addWidget(ventana)
    ventana.tipo_reporte.setCurrentText("Inventario Actual")
    ventana.formato_reporte.setCurrentText("Excel")
    ventana.generar_reporte()

    assert os.path.exists('reporte_inventario_actual.xlsx')

def test_generar_reporte_inventario_pdf(session, app, qtbot):
    # Añadir datos de prueba
    producto = Inventario(
        nombre_producto="Producto Test",
        descripcion="Descripción Test",
        categoria="Categoría Test",
        tipo="producto",
        unidad_medida="pieza",
        precio=10.0,
        codigo_barras="1234567890123",
        cantidad_stock=100,
        activo=True
    )
    session.add(producto)
    session.commit()

    ventana = VentanaReportes()
    qtbot.addWidget(ventana)
    ventana.tipo_reporte.setCurrentText("Inventario Actual")
    ventana.formato_reporte.setCurrentText("PDF")
    ventana.generar_reporte()

    assert os.path.exists('reporte_inventario_actual.pdf')

def test_generar_reporte_movimientos_excel(session, app, qtbot):
    # Añadir datos de prueba
    producto = Inventario(
        nombre_producto="Producto Test",
        descripcion="Descripción Test",
        categoria="Categoría Test",
        tipo="producto",
        unidad_medida="pieza",
        precio=10.0,
        codigo_barras="1234567890123",
        cantidad_stock=100,
        activo=True
    )
    session.add(producto)
    session.commit()

    movimiento = MovimientoInventario(
        producto_id=producto.id,
        tipo_movimiento="entrada",
        cantidad=50,
        descripcion="Movimiento Test"
    )
    session.add(movimiento)
    session.commit()

    ventana = VentanaReportes()
    qtbot.addWidget(ventana)
    ventana.tipo_reporte.setCurrentText("Movimientos de Inventario")
    ventana.formato_reporte.setCurrentText("Excel")
    ventana.generar_reporte()

    assert os.path.exists('reporte_movimientos_inventario.xlsx')

def test_generar_reporte_movimientos_pdf(session, app, qtbot):
    # Añadir datos de prueba
    producto = Inventario(
        nombre_producto="Producto Test",
        descripcion="Descripción Test",
        categoria="Categoría Test",
        tipo="producto",
        unidad_medida="pieza",
        precio=10.0,
        codigo_barras="1234567890123",
        cantidad_stock=100,
        activo=True
    )
    session.add(producto)
    session.commit()

    movimiento = MovimientoInventario(
        producto_id=producto.id,
        tipo_movimiento="entrada",
        cantidad=50,
        descripcion="Movimiento Test"
    )
    session.add(movimiento)
    session.commit()

    ventana = VentanaReportes()
    qtbot.addWidget(ventana)
    ventana.tipo_reporte.setCurrentText("Movimientos de Inventario")
    ventana.formato_reporte.setCurrentText("PDF")
    ventana.generar_reporte()

    assert os.path.exists('reporte_movimientos_inventario.pdf')