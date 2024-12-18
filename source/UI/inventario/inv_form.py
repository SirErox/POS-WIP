### **Formulario para Agregar/Editar Productos**
from PyQt5.QtWidgets import (
    QPushButton, QHBoxLayout, QDialog, QFormLayout, QLineEdit,
    QComboBox, QSpinBox, QMessageBox
)
from ...database.crud import agregar_producto, actualizar_producto,buscar_producto
class FormularioProducto(QDialog):
    def __init__(self, db, modo="agregar", producto_id=None):
        super().__init__()
        self.db = db
        self.modo = modo
        self.producto_id = producto_id
        self.setWindowTitle("Agregar Producto" if modo == "agregar" else "Editar Producto")
        self.resize(400, 300)
        
        layout = QFormLayout(self)
        
        # Campos del formulario
        self.nombre = QLineEdit()
        self.descripcion = QLineEdit()
        self.categoria = QLineEdit()
        self.tipo = QComboBox()
        self.tipo.addItems(["Físico", "Servicio"])
        self.unidad = QLineEdit()
        self.precio = QLineEdit()
        self.codigo_barras = QLineEdit()
        self.cantidad = QSpinBox()
        self.cantidad.setRange(0, 100000)
        self.activo = QComboBox()
        self.activo.addItems(["Sí", "No"])
        
        layout.addRow("Nombre:", self.nombre)
        layout.addRow("Descripción:", self.descripcion)
        layout.addRow("Categoría:", self.categoria)
        layout.addRow("Tipo:", self.tipo)
        layout.addRow("Unidad de Medida:", self.unidad)
        layout.addRow("Precio:", self.precio)
        layout.addRow("Código de Barras:", self.codigo_barras)
        layout.addRow("Cantidad:", self.cantidad)
        layout.addRow("Activo:", self.activo)
        
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
        if modo == "editar":
            self.cargar_datos()

    def cargar_datos(self):
        #Carga los datos del producto en los campos del formulario.
        try:
            producto = buscar_producto(self.db, self.producto_id)[0]
            self.nombre.setText(producto["nombre"])
            self.descripcion.setText(producto["descripcion"])
            self.categoria.setText(producto["categoria"])
            self.tipo.setCurrentText("Físico" if producto["tipo"] == "Físico" else "Servicio")
            self.unidad.setText(producto["unidad_medida"])
            self.precio.setText(str(producto["precio"]))
            self.codigo_barras.setText(producto["codigo_barras"])
            self.cantidad.setValue(producto["cantidad"])
            self.activo.setCurrentText("Sí" if producto["activo"] else "No")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {e}")

    def guardar_producto(self):
        #Guarda o actualiza el producto en la base de datos.
        try:
            if self.modo == "agregar":
                agregar_producto(
                    self.db,
                    self.nombre.text(),
                    self.descripcion.text(),
                    self.categoria.text(),
                    self.tipo.currentText(),
                    self.unidad.text(),
                    float(self.precio.text()),
                    self.codigo_barras.text(),
                    self.cantidad.value(),
                    self.activo.currentText() == "Sí"
                )
                QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
            else:
                actualizar_producto(
                    self.db,
                    self.producto_id,
                    nombre=self.nombre.text(),
                    descripcion=self.descripcion.text(),
                    categoria=self.categoria.text(),
                    tipo=self.tipo.currentText(),
                    unidad_medida=self.unidad.text(),
                    precio=float(self.precio.text()),
                    codigo_barras=self.codigo_barras.text(),
                    cantidad=self.cantidad.value(),
                    activo=self.activo.currentText() == "Sí"
                )
                QMessageBox.information(self, "Éxito", "Producto actualizado correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el producto: {e}")