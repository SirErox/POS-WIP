from PyQt5.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QHBoxLayout, QLineEdit, QComboBox, QDialog, QSpinBox, QLabel,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ...UI.inventario.inv_form import FormularioProducto
from ...database.database import SessionLocal
from ...database.models import Inventario
from ...database.crud import actualizar_producto

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
        self.tabla_inventario.setColumnCount(8)
        self.tabla_inventario.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Categoría", "Cantidad", "Foto", "Actualizar Stock", "Acciones"])
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
            
            # Mostrar foto
            if producto.foto:
                foto_label = QLabel()
                foto_label.setPixmap(QPixmap(producto.foto).scaled(50, 50, Qt.KeepAspectRatio))
                self.tabla_inventario.setCellWidget(row, 5, foto_label)
            else:
                self.tabla_inventario.setItem(row, 5, QTableWidgetItem("N/A"))
            
            # Campo para actualizar stock
            if producto.tipo == "producto":
                spinbox = QSpinBox()
                spinbox.setRange(0, 100000)
                spinbox.setValue(producto.cantidad_stock)
                spinbox.valueChanged.connect(lambda value, producto_id=producto.id: self.actualizar_stock(producto_id, value))
                self.tabla_inventario.setCellWidget(row, 6, spinbox)
            else:
                self.tabla_inventario.setItem(row, 6, QTableWidgetItem("N/A"))
            
            # Botón para editar producto
            boton_editar = QPushButton("Editar")
            boton_editar.clicked.connect(lambda checked, producto_id=producto.id: self.editar_producto(producto_id))
            self.tabla_inventario.setCellWidget(row, 7, boton_editar)
        
        session.close()

    def actualizar_stock(self, producto_id, cantidad):
        session = SessionLocal()
        try:
            actualizar_producto(session, producto_id, cantidad_stock=cantidad)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el stock: {e}")
        finally:
            session.close()

    def agregar_producto(self):
        form = FormularioProducto()
        if form.exec_() == QDialog.Accepted:
            self.actualizar_tabla()

    def editar_producto(self, producto_id):
        form = FormularioProducto(producto_id)
        if form.exec_() == QDialog.Accepted:
            self.actualizar_tabla()
