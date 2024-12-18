from PyQt5.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QHBoxLayout, QLineEdit, QComboBox, QDialog
)
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
        
        titulo = QLabel("Gestión de Inventario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        # Controles de búsqueda
        self.barra_busqueda = QLineEdit()
        self.barra_busqueda.setPlaceholderText("Buscar por nombre...")
        self.barra_busqueda.textChanged.connect(self.actualizar_tabla)
        
        self.combo_categoria = QComboBox()
        self.combo_categoria.addItem("Todas las categorías")
        self.combo_categoria.addItems(self.obtener_categorias())
        self.combo_categoria.currentTextChanged.connect(self.actualizar_tabla)
        
        busqueda_layout = QHBoxLayout()
        busqueda_layout.addWidget(self.barra_busqueda)
        busqueda_layout.addWidget(self.combo_categoria)
        layout.addLayout(busqueda_layout)
        
        # Tabla de inventario
        self.tabla_inventario = QTableWidget()
        self.tabla_inventario.setColumnCount(5)
        self.tabla_inventario.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Categoría", "Cantidad"])
        layout.addWidget(self.tabla_inventario)
        
        # Botones de acción
        botones_layout = QHBoxLayout()
        self.boton_agregar = QPushButton("Agregar Producto")
        self.boton_agregar.clicked.connect(self.agregar_producto)
        botones_layout.addWidget(self.boton_agregar)
        layout.addLayout(botones_layout)
        
        self.setLayout(layout)
        self.actualizar_tabla()

    def obtener_categorias(self):
        session = SessionLocal()
        categorias = session.query(Inventario.categoria).distinct().all()
        session.close()
        return [categoria[0] for categoria in categorias]

    def actualizar_tabla(self):
        session = SessionLocal()
        query = session.query(Inventario)
        
        # Filtrar por nombre
        nombre_filtro = self.barra_busqueda.text()
        if nombre_filtro:
            query = query.filter(Inventario.nombre_producto.ilike(f"%{nombre_filtro}%"))
        
        # Filtrar por categoría
        categoria_filtro = self.combo_categoria.currentText()
        if categoria_filtro != "Todas las categorías":
            query = query.filter(Inventario.categoria == categoria_filtro)
        
        productos = query.all()
        self.tabla_inventario.setRowCount(len(productos))
        
        for row, producto in enumerate(productos):
            self.tabla_inventario.setItem(row, 0, QTableWidgetItem(str(producto.id)))
            self.tabla_inventario.setItem(row, 1, QTableWidgetItem(producto.nombre_producto))
            self.tabla_inventario.setItem(row, 2, QTableWidgetItem(producto.descripcion))
            self.tabla_inventario.setItem(row, 3, QTableWidgetItem(producto.categoria))
            self.tabla_inventario.setItem(row, 4, QTableWidgetItem(str(producto.cantidad_stock)))
        
        session.close()

    def agregar_producto(self):
        form = FormularioProducto()
        if form.exec_() == QDialog.Accepted:
            self.actualizar_tabla()
