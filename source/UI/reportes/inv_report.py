from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox, QDateEdit, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from ...database.database import SessionLocal
from ...database.models import Inventario, MovimientoInventario
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from source.Utils.auditoria import registrar_accion

class VentanaReportes(QWidget):
    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id
        self.setWindowTitle("Generar Reportes de Inventario")
        self.resize(400, 300)
        layout = QVBoxLayout(self)
        
        titulo = QLabel("Generar Reportes de Inventario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        # Controles de selección de reporte
        self.tipo_reporte = QComboBox()
        self.tipo_reporte.addItems(["Inventario Actual", "Movimientos de Inventario"])
        self.formato_reporte = QComboBox()
        self.formato_reporte.addItems(["Excel", "PDF"])
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setDate(QDate.currentDate().addMonths(-1))
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setDate(QDate.currentDate())
        self.fecha_fin.setCalendarPopup(True)
        
        layout.addWidget(QLabel("Tipo de Reporte:"))
        layout.addWidget(self.tipo_reporte)
        layout.addWidget(QLabel("Formato de Reporte:"))
        layout.addWidget(self.formato_reporte)
        layout.addWidget(QLabel("Fecha Inicio:"))
        layout.addWidget(self.fecha_inicio)
        layout.addWidget(QLabel("Fecha Fin:"))
        layout.addWidget(self.fecha_fin)
        
        # Botón para generar reporte
        self.boton_generar = QPushButton("Generar Reporte")
        self.boton_generar.clicked.connect(self.generar_reporte)
        layout.addWidget(self.boton_generar)
        
        self.setLayout(layout)

    def generar_reporte(self):
        tipo_reporte = self.tipo_reporte.currentText()
        formato_reporte = self.formato_reporte.currentText()
        fecha_inicio = self.fecha_inicio.date().toString("yyyy-MM-dd")
        fecha_fin = self.fecha_fin.date().toString("yyyy-MM-dd")
        
        session = SessionLocal()
        try:
            if tipo_reporte == "Inventario Actual":
                productos = session.query(Inventario).all()
                data = [{
                    'ID': producto.id,
                    'Nombre': producto.nombre_producto,
                    'Descripción': producto.descripcion,
                    'Categoría': producto.categoria,
                    'Cantidad': producto.cantidad_stock,
                    'Precio': producto.precio
                } for producto in productos]
                if formato_reporte == "Excel":
                    wb = Workbook()
                    ws = wb.active
                    ws.append(['ID', 'Nombre', 'Descripción', 'Categoría', 'Cantidad', 'Precio'])
                    for row in data:
                        ws.append([row['ID'], row['Nombre'], row['Descripción'], row['Categoría'], row['Cantidad'], row['Precio']])
                    wb.save('reporte_inventario_actual.xlsx')
                elif formato_reporte == "PDF":
                    c = canvas.Canvas("reporte_inventario_actual.pdf", pagesize=letter)
                    width, height = letter
                    y = height - 40
                    for row in data:
                        for key, value in row.items():
                            c.drawString(30, y, f"{key}: {value}")
                            y -= 20
                        y -= 20
                    c.save()
                QMessageBox.information(self, "Éxito", f"Reporte de Inventario Actual generado en formato {formato_reporte}.")
            elif tipo_reporte == "Movimientos de Inventario":
                movimientos = session.query(MovimientoInventario).filter(
                    MovimientoInventario.fecha_movimiento.between(fecha_inicio, fecha_fin)
                ).all()
                data = [{
                    'ID': movimiento.id,
                    'Producto': movimiento.producto.nombre_producto,
                    'Tipo': movimiento.tipo_movimiento,
                    'Cantidad': movimiento.cantidad,
                    'Fecha': movimiento.fecha_movimiento.strftime("%Y-%m-%d %H:%M:%S"),
                    'Descripción': movimiento.descripcion
                } for movimiento in movimientos]
                if formato_reporte == "Excel":
                    wb = Workbook()
                    ws = wb.active
                    ws.append(['ID', 'Producto', 'Tipo', 'Cantidad', 'Fecha', 'Descripción'])
                    for row in data:
                        ws.append([row['ID'], row['Producto'], row['Tipo'], row['Cantidad'], row['Fecha'], row['Descripción']])
                    wb.save('reporte_movimientos_inventario.xlsx')
                elif formato_reporte == "PDF":
                    c = canvas.Canvas("reporte_movimientos_inventario.pdf", pagesize=letter)
                    width, height = letter
                    y = height - 40
                    for row in data:
                        for key, value in row.items():
                            c.drawString(30, y, f"{key}: {value}")
                            y -= 20
                        y -= 20
                    c.save()
                QMessageBox.information(self, "Éxito", f"Reporte de Movimientos de Inventario generado en formato {formato_reporte}.")
            
            # Registrar acción en auditoría
            registrar_accion(self.usuario_id, "Generar Reporte", f"Reporte de {tipo_reporte} generado en formato {formato_reporte}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el reporte: {e}")
        finally:
            session.close()