from PyQt5.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QHBoxLayout, QLineEdit, QComboBox, QDialog,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from source.database.database import SessionLocal
from source.database.models import Inventario, Proveedor, ProductoProveedor
from ...database.crud import actualizar_producto, eliminar_producto, agregar_proveedor_producto
from ...UI.inventario.inv_mov import VentanaMovimientos
from ...UI.reportes.inv_report import VentanaReportes
from ...UI.inventario.inv_form import FormularioProducto

class VentanaInventario(QWidget):
    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id
        self.setWindowTitle("Gestión de Inventario")
        self.setWindowIcon(QIcon('source/icons/logo.jpeg'))
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout(self)
        
        # Título
        titulo = QLabel("Gestión de Inventario")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        # Botones superiores
        botones_superiores_layout = QHBoxLayout()
        self.boton_movimientos = QPushButton("Ver Movimientos")
        self.boton_movimientos.clicked.connect(self.abrir_ventana_movimientos)
        self.boton_reportes = QPushButton("Generar Reportes")
        self.boton_reportes.clicked.connect(self.abrir_ventana_reportes)
        botones_superiores_layout.addWidget(self.boton_movimientos)
        botones_superiores_layout.addWidget(self.boton_reportes)
        layout.addLayout(botones_superiores_layout)
        
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
        self.tabla_inventario.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Categoría", "Cantidad", "Editar", "Eliminar", "Proveedores"])
        self.tabla_inventario.cellClicked.connect(self.cargar_proveedores_producto)
        layout.addWidget(self.tabla_inventario)
        
        #Botones de gestión de productos
        botones_layout = QHBoxLayout()
        self.boton_agregar = QPushButton("Agregar Producto")
        self.boton_agregar.clicked.connect(self.agregar_producto)
        botones_layout.addWidget(self.boton_agregar)
        layout.addLayout(botones_layout)


        # Tabla de proveedores asociados
        self.label_proveedores = QLabel("Proveedores Asociados:")
        self.label_proveedores.setStyleSheet("font-size: 16px; margin-top: 10px;")
        layout.addWidget(self.label_proveedores)
        
        self.tabla_proveedores = QTableWidget()
        self.tabla_proveedores.setColumnCount(4)
        self.tabla_proveedores.setHorizontalHeaderLabels(["ID", "Proveedor", "Precio Compra", "Tiempo de Entrega"])
        layout.addWidget(self.tabla_proveedores)
        
        # Botones de gestión de proveedores
        botones_proveedores_layout = QHBoxLayout()
        self.boton_agregar_proveedor = QPushButton("Agregar Proveedor")
        self.boton_agregar_proveedor.clicked.connect(self.agregar_proveedor_producto)
        self.boton_editar_proveedor = QPushButton("Editar Relación")
        self.boton_editar_proveedor.clicked.connect(self.editar_proveedor_producto)
        self.boton_eliminar_proveedor = QPushButton("Eliminar Relación")
        self.boton_eliminar_proveedor.clicked.connect(self.eliminar_proveedor_producto)
        botones_proveedores_layout.addWidget(self.boton_agregar_proveedor)
        botones_proveedores_layout.addWidget(self.boton_editar_proveedor)
        botones_proveedores_layout.addWidget(self.boton_eliminar_proveedor)
        layout.addLayout(botones_proveedores_layout)
        
        # Configuración final
        self.setLayout(layout)
        self.actualizar_tabla()

    def abrir_ventana_movimientos(self):
        self.ventana_movimientos = VentanaMovimientos()
        self.ventana_movimientos.show()

    def abrir_ventana_reportes(self):
        self.ventana_reportes = VentanaReportes(self.usuario_id)
        self.ventana_reportes.show()

    def obtener_categorias(self):
        session = SessionLocal()
        categorias = session.query(Inventario.categoria).distinct().all()
        session.close()
        return [categoria[0] for categoria in categorias]

    def agregar_producto(self):
        form = FormularioProducto()
        if form.exec_() == QDialog.Accepted:
            self.actualizar_tabla()
    
    def actualizar_stock(self, producto_id, cantidad):
        session = SessionLocal()
        try:
            actualizar_producto(session, producto_id, cantidad_stock=cantidad)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el stock: {e}")
        finally:
            session.close()

    def editar_producto(self, producto_id):
        form = FormularioProducto(producto_id)
        if form.exec_() == QDialog.Accepted:
            self.actualizar_tabla()

    def eliminar_producto(self, producto_id):
        """Elimina un producto del inventario."""
        session = SessionLocal()
        try:
            producto = session.query(Inventario).filter(Inventario.id == producto_id).first()
            if producto:
                session.delete(producto)
                session.commit()
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
                self.actualizar_tabla()
            else:
                QMessageBox.warning(self, "Error", "Producto no encontrado.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Error al eliminar el producto: {e}")
        finally:
            session.close()

    def actualizar_tabla(self):
        session = SessionLocal()
        productos = session.query(Inventario).all()
        self.tabla_inventario.setRowCount(0)
        for producto in productos:
            row_position = self.tabla_inventario.rowCount()
            self.tabla_inventario.insertRow(row_position)
            self.tabla_inventario.setItem(row_position, 0, QTableWidgetItem(str(producto.id)))
            self.tabla_inventario.setItem(row_position, 1, QTableWidgetItem(producto.nombre_producto))
            self.tabla_inventario.setItem(row_position, 2, QTableWidgetItem(producto.descripcion))
            self.tabla_inventario.setItem(row_position, 3, QTableWidgetItem(producto.categoria))
            self.tabla_inventario.setItem(row_position, 4, QTableWidgetItem(str(producto.cantidad_stock)))
            boton_editar = QPushButton("Editar")
            boton_editar.clicked.connect(lambda _, id=producto.id: self.editar_producto(id))
            self.tabla_inventario.setCellWidget(row_position, 5, boton_editar)
            boton_eliminar = QPushButton("Eliminar")
            boton_eliminar.clicked.connect(lambda _, id=producto.id: self.eliminar_producto(id))
            self.tabla_inventario.setCellWidget(row_position, 6, boton_eliminar)
            boton_ver_proveedores = QPushButton("Proveedores")
            boton_ver_proveedores.clicked.connect(lambda _, id=producto.id: self.cargar_proveedores_producto(id))
            self.tabla_inventario.setCellWidget(row_position, 7, boton_ver_proveedores)
        session.close()

    def cargar_proveedores_producto(self, producto_id):
        session = SessionLocal()
        relaciones = session.query(ProductoProveedor).filter_by(producto_id=producto_id).all()
        self.tabla_proveedores.setRowCount(0)
        for relacion in relaciones:
            proveedor = session.query(Proveedor).filter_by(id=relacion.proveedor_id).first()
            row_position = self.tabla_proveedores.rowCount()
            self.tabla_proveedores.insertRow(row_position)
            self.tabla_proveedores.setItem(row_position, 0, QTableWidgetItem(str(proveedor.id)))
            self.tabla_proveedores.setItem(row_position, 1, QTableWidgetItem(proveedor.nombre))
            self.tabla_proveedores.setItem(row_position, 2, QTableWidgetItem(str(relacion.precio_compra)))
            self.tabla_proveedores.setItem(row_position, 3, QTableWidgetItem(relacion.tiempo_entrega))
        session.close()

    def agregar_proveedor_producto(self):
        print("Agregar proveedor a producto")

    def editar_proveedor_producto(self):
        print("Editar proveedor de producto")

    def eliminar_proveedor_producto(self):
        print("Eliminar proveedor de producto")