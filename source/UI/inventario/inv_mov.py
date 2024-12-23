from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ...database.database import SessionLocal
from ...database.models import MovimientoInventario

class VentanaMovimientos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movimientos de Inventario")
        self.setWindowIcon(QIcon('source/icons/logo.jpeg'))
        self.resize(800, 600)
        layout = QVBoxLayout(self)
        
        titulo = QLabel("Movimientos de Inventario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        # Tabla de movimientos
        self.tabla_movimientos = QTableWidget()
        self.tabla_movimientos.setColumnCount(5)
        self.tabla_movimientos.setHorizontalHeaderLabels(["ID", "Producto", "Tipo", "Cantidad", "Fecha"])
        layout.addWidget(self.tabla_movimientos)
        
        self.setLayout(layout)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        session = SessionLocal()
        movimientos = session.query(MovimientoInventario).all()
        self.tabla_movimientos.setRowCount(len(movimientos))
        
        for row, movimiento in enumerate(movimientos):
            self.tabla_movimientos.setItem(row, 0, QTableWidgetItem(str(movimiento.id)))
            self.tabla_movimientos.setItem(row, 1, QTableWidgetItem(movimiento.producto.nombre_producto))
            self.tabla_movimientos.setItem(row, 2, QTableWidgetItem(movimiento.tipo_movimiento))
            self.tabla_movimientos.setItem(row, 3, QTableWidgetItem(str(movimiento.cantidad)))
            self.tabla_movimientos.setItem(row, 4, QTableWidgetItem(movimiento.fecha_movimiento.strftime("%Y-%m-%d %H:%M:%S")))
        
        session.close()