import os
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox, QPushButton, QHBoxLayout, QMessageBox, QLabel, QFileDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ...database.database import SessionLocal
from ...database.crud import agregar_producto, actualizar_producto, buscar_producto

class FormularioProducto(QDialog):
    def __init__(self, producto_id=None):
        super().__init__()
        self.producto_id = producto_id
        self.setWindowTitle("Agregar Producto" if producto_id is None else "Editar Producto")
        self.resize(400, 400)
         #quitar icono ? de la ventana
        self.setWindowFlags(
        Qt.Window |
        Qt.CustomizeWindowHint |
        Qt.WindowTitleHint |
        Qt.WindowCloseButtonHint 
        )
        
        layout = QFormLayout(self)
        
        # Campos del formulario
        self.nombre = QLineEdit()
        self.descripcion = QLineEdit()
        self.categoria = QLineEdit()
        self.tipo = QComboBox()
        self.tipo.addItems(["producto", "servicio"])
        self.unidad = QLineEdit()
        self.precio = QLineEdit()
        self.codigo_barras = QLineEdit()
        self.cantidad = QSpinBox()
        self.cantidad.setRange(0, 100000)
        self.activo = QComboBox()
        self.activo.addItems(["Sí", "No"])
        
        # Campo para la foto
        self.foto_label = QLabel()
        self.foto_label.setFixedSize(100, 100)
        self.foto_label.setStyleSheet("border: 1px solid black;")
        self.boton_cargar_foto = QPushButton("Cargar Foto")
        self.boton_cargar_foto.clicked.connect(self.cargar_foto)
        self.foto_path = None
        
        layout.addRow("Nombre:", self.nombre)
        layout.addRow("Descripción:", self.descripcion)
        layout.addRow("Categoría:", self.categoria)
        layout.addRow("Tipo:", self.tipo)
        layout.addRow("Unidad de Medida:", self.unidad)
        layout.addRow("Precio:", self.precio)
        layout.addRow("Código de Barras:", self.codigo_barras)
        layout.addRow("Cantidad:", self.cantidad)
        layout.addRow("Activo:", self.activo)
        layout.addRow("Foto:", self.foto_label)
        layout.addRow("", self.boton_cargar_foto)
        
        # Botones de acción
        botones_layout = QHBoxLayout()
        self.boton_guardar = QPushButton("Guardar")
        self.boton_cancelar = QPushButton("Cancelar")
        botones_layout.addWidget(self.boton_guardar)
        botones_layout.addWidget(self.boton_cancelar)
        layout.addRow(botones_layout)
        
        self.boton_guardar.clicked.connect(self.guardar_producto)
        self.boton_cancelar.clicked.connect(self.reject)
        
        # Si es modo editar, carga los datos existentes
        if producto_id is not None:
            self.cargar_datos()

    def cargar_datos(self):
        session = SessionLocal()
        try:
            producto = buscar_producto(session, self.producto_id)
            self.nombre.setText(producto.nombre_producto)
            self.descripcion.setText(producto.descripcion)
            self.categoria.setText(producto.categoria)
            self.tipo.setCurrentText(producto.tipo)
            self.unidad.setText(producto.unidad_medida)
            self.precio.setText(str(producto.precio))
            self.codigo_barras.setText(producto.codigo_barras)
            self.cantidad.setValue(producto.cantidad_stock)
            self.activo.setCurrentText("Sí" if producto.activo else "No")
            if producto.foto:
                self.foto_path = producto.foto
                self.foto_label.setPixmap(QPixmap(producto.foto).scaled(100, 100, Qt.KeepAspectRatio))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {e}")
        finally:
            session.close()

    def cargar_foto(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.foto_path = file_name
            self.foto_label.setPixmap(QPixmap(file_name).scaled(100, 100, Qt.KeepAspectRatio))

    def guardar_producto(self):
        session = SessionLocal()
        try:
            nombre_producto = self.nombre.text()
            if self.foto_path:
                # Obtener la extensión del archivo
                _, extension = os.path.splitext(self.foto_path)
                # Renombrar la foto
                nueva_foto_path = f"fotos/{nombre_producto}_item{extension}"
                # Crear el directorio si no existe
                os.makedirs(os.path.dirname(nueva_foto_path), exist_ok=True)
                # Guardar la foto en la nueva ubicación
                os.rename(self.foto_path, nueva_foto_path)
                self.foto_path = nueva_foto_path

            if self.producto_id is None:
                agregar_producto(
                    session,
                    nombre_producto,
                    self.descripcion.text(),
                    self.categoria.text(),
                    self.tipo.currentText(),
                    self.unidad.text(),
                    float(self.precio.text()),
                    self.codigo_barras.text(),
                    self.cantidad.value(),
                    self.activo.currentText() == "Sí",
                    self.foto_path
                )
                QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
            else:
                actualizar_producto(
                    session,
                    self.producto_id,
                    nombre_producto=nombre_producto,
                    descripcion=self.descripcion.text(),
                    categoria=self.categoria.text(),
                    tipo=self.tipo.currentText(),
                    unidad_medida=self.unidad.text(),
                    precio=float(self.precio.text()),
                    codigo_barras=self.codigo_barras.text(),
                    cantidad_stock=self.cantidad.value(),
                    activo=self.activo.currentText() == "Sí",
                    foto=self.foto_path
                )
                QMessageBox.information(self, "Éxito", "Producto actualizado correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el producto: {e}")
        finally:
            session.close()