from PyQt5.QtWidgets import( QLabel,QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                            QPushButton, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from ...UI.inventario.inv_form import FormularioProducto
from ...database.database import SessionLocal
from ...database.models import Inventario

class VentanaInventario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Inventario")
        self.resize(800, 600)
        layout = QVBoxLayout(self)
        titulo=QLabel("Gestion de inventario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(10)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Descripción", "Categoría", "Tipo", 
            "Unidad", "Precio", "Código de Barras", "Cantidad", "Activo"
        ])
        layout.addWidget(self.tabla)

        botones_layout = QHBoxLayout()
        self.boton_agregar = QPushButton("Agregar Producto")
        self.boton_editar = QPushButton("Editar Producto")
        self.boton_eliminar = QPushButton("Eliminar Producto")

        botones_layout.addWidget(self.boton_agregar)
        botones_layout.addWidget(self.boton_editar)
        botones_layout.addWidget(self.boton_eliminar)
        layout.addLayout(botones_layout)

        self.boton_agregar.clicked.connect(self.abrir_formulario_agregar)
        self.boton_editar.clicked.connect(self.abrir_formulario_editar)
        self.boton_eliminar.clicked.connect(self.eliminar_producto)

        self.cargar_datos()

    def cargar_datos(self):
        session=SessionLocal()
        productos = session.query(Inventario).all()
        self.tabla.setRowCount(len(productos))
        for row, producto in enumerate(productos):
            self.tabla.setItem(row, 0, QTableWidgetItem(str(producto.id)))
            self.tabla.setItem(row, 1, QTableWidgetItem(producto.nombre_producto))
            self.tabla.setItem(row, 2, QTableWidgetItem(producto.descripcion or ""))
            self.tabla.setItem(row, 3, QTableWidgetItem(producto.categoria or ""))
            self.tabla.setItem(row, 4, QTableWidgetItem(producto.tipo))
            self.tabla.setItem(row, 5, QTableWidgetItem(producto.unidad_medida or ""))
            self.tabla.setItem(row, 6, QTableWidgetItem(str(producto.precio)))
            self.tabla.setItem(row, 7, QTableWidgetItem(producto.codigo_barras or ""))
            self.tabla.setItem(row, 8, QTableWidgetItem(str(producto.cantidad_stock)))
            self.tabla.setItem(row, 9, QTableWidgetItem("Sí" if producto.activo else "No"))

    def abrir_formulario_agregar(self):
        dialogo = FormularioProducto()
        if dialogo.exec_():
            self.cargar_datos()

    def abrir_formulario_editar(self):
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Selecciona un producto para editar.")
            return
        producto_id = int(self.tabla.item(fila_seleccionada, 0).text())
        dialogo = FormularioProducto(producto_id=producto_id)
        if dialogo.exec_():
            self.cargar_datos()

    def eliminar_producto(self):
        session=SessionLocal()
        fila_seleccionada = self.tabla.currentRow()
        if fila_seleccionada == -1:
            QMessageBox.warning(self, "Advertencia", "Selecciona un producto para eliminar.")
            return
        producto_id = int(self.tabla.item(fila_seleccionada, 0).text())
        producto = session.query(Inventario).get(producto_id)
        session.delete(producto)
        session.commit()
        self.cargar_datos()
