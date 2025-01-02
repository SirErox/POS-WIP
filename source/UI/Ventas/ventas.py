# Importaciones de PyQt5
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QHeaderView, QScrollArea, QWidget, QFrame, QMessageBox,
    QInputDialog, QTableWidgetItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

# Iconos con qtawesome
from qtawesome import icon

# Base de datos
from source.database.database import SessionLocal
from source.database.models import Inventario

class VentasWindow(QMainWindow):
    def __init__(self, app_manager, usuario):
        super().__init__()
        self.app_manager = app_manager
        self.usuario = usuario
        #Configuración inicial de la ventana
        self.setWindowTitle("Ventas - POS System")
        self.setWindowIcon(QIcon('source/icons/logo.jpeg'))
        self.resize(720, 576)

       # Layout principal
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout(self.centralWidget)

        # Sección izquierda (tabla y carrusel)
        self.leftSection = QVBoxLayout()

        # Barra de búsqueda
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Buscar productos...")
        self.searchBar.textChanged.connect(self.filtrar_productos)
        self.leftSection.addWidget(self.searchBar)
        self.searchBar.show()


        # Tabla de carrito
        self.cartTable = QTableWidget()
        self.cartTable.setColumnCount(4)
        self.cartTable.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio",""])
        self.cartTable.setFrameShape(QFrame.Box)
        self.cartTable.setObjectName("cartTable")
        self.cartTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # La columna de Producto será más ancha
        self.cartTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.cartTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.cartTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.cartTable.cellDoubleClicked.connect(self.cambiar_cantidad_por_doble_click)
        self.leftSection.addWidget(self.cartTable)

        # Barra inferior (carrusel)
        self.carrusel = QWidget()
        self.carrusel.setObjectName("carrusel")
        self.carrusel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.carrusel.hide()
        self.carrusellayout = QVBoxLayout(self.carrusel)

        # Área deslizante de productos
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedHeight(150)  # Reducir la altura del carrusel
        self.productContainer = QWidget()
        self.productLayout = QHBoxLayout(self.productContainer)
        self.scrollArea.setWidget(self.productContainer)
        self.carrusellayout.addWidget(self.scrollArea)

        # Botones de navegación dentro del carrusel
        self.navButtonsLayout = QHBoxLayout()
        self.prevButton = QPushButton()
        self.prevButton.setIcon(icon("fa.arrow-left"))
        self.nextButton = QPushButton()
        self.nextButton.setIcon(icon("fa.arrow-right"))
        self.prevButton.setObjectName("navButton")
        self.nextButton.setObjectName("navButton")
        self.prevButton.clicked.connect(self.mover_izquierda)
        self.nextButton.clicked.connect(self.mover_derecha)
        self.navButtonsLayout.addWidget(self.prevButton)
        self.navButtonsLayout.addWidget(self.nextButton)
        self.carrusellayout.addLayout(self.navButtonsLayout)

        self.leftSection.addWidget(self.carrusel)
        self.mainLayout.addLayout(self.leftSection)

        # Sección derecha (total del carrito)
        self.rightSection = QVBoxLayout()

        # Total del carrito
        self.totalLabel = QLabel("Total: $0.00")
        self.totalLabel.setAlignment(Qt.AlignRight)
        self.totalLabel.setObjectName("totalLabel")
        self.rightSection.addWidget(self.totalLabel)

        # Botón de finalizar venta
        self.finalizarVentaButton = QPushButton("Finalizar Venta")
        self.finalizarVentaButton.setObjectName("finalizarVentaButton")
        self.finalizarVentaButton.clicked.connect(self.finalizar_venta)
        self.rightSection.addWidget(self.finalizarVentaButton)

        self.mainLayout.addLayout(self.rightSection)

        self.mostrar_productos()

    def filtrar_productos(self):
        texto_busqueda = self.searchBar.text().lower()
        # Filtrar productos por texto de busqueda
        if texto_busqueda:
            productos_filtrados = [
                producto for producto in self.productos
                if texto_busqueda in producto["nombre"].lower()
            ]
        else:
            productos_filtrados = []
        
        # Mostrar u ocultar el carrusel según el resultado de la búsqueda
        if productos_filtrados:
            self.actualizar_carrusel(productos_filtrados)
            self.carrusel.show()
        else:
            self.carrusel.hide()

    def actualizar_carrusel(self, productos_filtrados):
        # Limpiar el layout del carrusel
        for i in reversed(range(self.productLayout.count())):
            widget = self.productLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Agregar los productos filtrados al carrusel
        for producto in productos_filtrados:
            imagen_ruta = producto['imagen'] if producto['imagen'] else 'source/imagenes/productos/default_item.jpeg'

            frame = QWidget()
            frame.setFixedSize(100, 140)
            frameLayout = QVBoxLayout(frame)
            frameLayout.setContentsMargins(2, 2, 2, 2)

            # Imagen del producto
            imagen_label = QLabel()
            try:
                pixmap = QPixmap(imagen_ruta).scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                imagen_label.setPixmap(pixmap)
            except Exception as e:
                pixmap = QPixmap('source/imagenes/productos/default_item.jpeg').scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                imagen_label.setPixmap(pixmap)

            imagen_label.mouseDoubleClickEvent = lambda event, p=producto: self.preguntar_cantidad(p)
            frameLayout.addWidget(imagen_label)

            # Nombre del producto
            nombre_label = QLabel(producto["nombre"])
            nombre_label.setAlignment(Qt.AlignCenter)
            nombre_label.setStyleSheet("font-size: 10pt;")
            nombre_label.setWordWrap(True)
            nombre_label.setFixedHeight(35)
            frameLayout.addWidget(nombre_label)

            # Botón para agregar al carrito
            botonAgregar = QPushButton("+")
            botonAgregar.setFixedSize(25, 25)
            botonAgregar.clicked.connect(lambda _, p=producto: self.preguntar_cantidad(p))
            frameLayout.addWidget(botonAgregar, alignment=Qt.AlignRight | Qt.AlignBottom)

            self.productLayout.addWidget(frame)

        self.productContainer.update()  # Actualiza el contenedor visualmente

    def cambiar_cantidad_por_doble_click(self, row, column):
        # Permitir edición solo en la columna de cantidad (índice 1)
        if column == 1:
            cantidad_actual = int(self.cartTable.item(row, column).text())
            nueva_cantidad, ok = QInputDialog.getInt(
                self,
                "Editar cantidad",
                f"Ingrese la nueva cantidad para {self.cartTable.item(row, 0).text()}:",
                cantidad_actual,
                1,  # Mínimo
                1000  # Máximo
            )
            if ok:
                self.cartTable.setItem(row, column, QTableWidgetItem(str(nueva_cantidad)))
                self.actualizar_total()
        else:
            QMessageBox.warning(self, "Edición no permitida", "Solo puede modificar la cantidad.")

    def finalizar_venta(self):  
        # 1. Validación del carrito
        if self.cartTable.rowCount() == 0:
            QMessageBox.warning(self, "Carrito vacío", "No hay productos en el carrito.")
            return

        # Recopilar los productos en el carrito
        items_carrito = []
        for row in range(self.cartTable.rowCount()):
            producto = self.cartTable.item(row, 0).text()
            cantidad = int(self.cartTable.item(row, 1).text())
            precio = float(self.cartTable.item(row, 2).text().strip("$").replace(",", ""))
            items_carrito.append({"nombre": producto, "cantidad": cantidad, "precio": precio})

        # 2. Validación del stock
        for item in items_carrito:
            producto = self.app_manager.crud.obtener_producto_por_nombre(item["nombre"])
            if not producto:
                QMessageBox.critical(self, "Error", f"El producto '{item['nombre']}' no existe en la base de datos.")
                return

            if producto.stock < item["cantidad"]:
                QMessageBox.warning(
                    self, 
                    "Stock insuficiente", 
                    f"El producto '{item['nombre']}' solo tiene {producto.stock} unidades disponibles."
                )
                return

        # 3. Seleccionar el método de pago
        metodos_pago = ["Efectivo", "Tarjeta", "Transferencia", "Otro"]
        metodo_pago, ok = QInputDialog.getItem(self, "Método de pago", "Seleccione un método de pago:", metodos_pago, editable=False)
        if not ok:
            return

        # 4. Confirmación de la venta
        confirmacion = QMessageBox.question(
            self, 
            "Confirmar Venta", 
            f"¿Desea finalizar la venta con un total de {self.totalLabel.text()}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmacion != QMessageBox.Yes:
            return

        # 5. Registrar la venta
        try:
            # Abrir una sesión de la base de datos
            session = SessionLocal()

            # Insertar en la tabla `ventas`
            venta_id = self.app_manager.crud.registrar_venta(
                session,
                usuario_id=self.usuario.id,
                metodo_pago=metodo_pago,
                total=float(self.totalLabel.text().strip("$").replace(",", ""))
            )

            # Insertar en la tabla `detalle_venta` y actualizar el stock
            for item in items_carrito:
                self.app_manager.crud.registrar_detalle_venta(
                    session,
                    venta_id=venta_id,
                    producto_nombre=item["nombre"],
                    cantidad=item["cantidad"],
                    precio=item["precio"]
                )
                # Actualizar el stock del producto
                self.app_manager.crud.actualizar_stock(
                    session,
                    producto_nombre=item["nombre"],
                    cantidad=-item["cantidad"]
                )

            session.commit()  # Confirmar cambios en la base de datos

            # 6. Feedback al usuario
            QMessageBox.information(self, "Venta Registrada", "La venta se registró exitosamente.")
            self.limpiar_carrito()  # Limpiar el carrito después de la venta
            self.actualizar_total()  # Reiniciar el total

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al registrar la venta: {str(e)}")
        finally:
            session.close()
    
    def limpiar_carrito(self):
        while self.cartTable.rowCount() > 0:
            self.cartTable.removeRow(0)
        self.actualizar_total()

    def mostrar_productos(self):
        # Obtener productos desde la base de datos
        session = SessionLocal()
        try:
            productos_db = session.query(Inventario).all()
            self.productos = [
                {"nombre": producto.nombre_producto, "imagen": producto.foto, "precio": producto.precio}
                for producto in productos_db
            ]
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los productos: {str(e)}")
            self.productos = []
        finally:
            session.close()

         # Limpiar el layout de productos
        for i in reversed(range(self.productLayout.count())):
            widget = self.productLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Mostrar productos en el carrusel
        for producto in self.productos:
            imagen_ruta = producto['imagen'] if producto['imagen'] else 'source/imagenes/productos/default_item.jpeg'
        
            frame = QWidget()
            frame.setFixedSize(100, 140)
            frameLayout = QVBoxLayout(frame)
            frameLayout.setContentsMargins(2, 2, 2, 2)

            # Imagen del producto
            imagen_label = QLabel()
            try:
                pixmap = QPixmap(imagen_ruta).scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                imagen_label.setPixmap(pixmap)
            except Exception as e:
                pixmap = QPixmap('source/imagenes/productos/default_item.jpeg').scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                imagen_label.setPixmap(pixmap)
            
            imagen_label.mouseDoubleClickEvent= lambda event, p=producto: self.preguntar_cantidad(p)
            frameLayout.addWidget(imagen_label)

            # Nombre del producto
            nombre_label = QLabel(producto["nombre"])
            nombre_label.setAlignment(Qt.AlignCenter)
            nombre_label.setStyleSheet("font-size: 10pt;")
            nombre_label.setWordWrap(True)
            nombre_label.setFixedHeight(35)
            frameLayout.addWidget(nombre_label)

            # Botón para agregar al carrito
            botonAgregar = QPushButton("+")
            botonAgregar.setFixedSize(25, 25)
            botonAgregar.clicked.connect(lambda _, p=producto: self.preguntar_cantidad(p))
            frameLayout.addWidget(botonAgregar, alignment=Qt.AlignRight | Qt.AlignBottom)

            self.productLayout.addWidget(frame)
        self.productContainer.update()  # Actualiza el contenedor visualmente

    def seleccionar_producto(self, texto):
        """Agregar el producto seleccionado desde el QCompleter."""
        nombre_producto = texto.split(" - ")[0]  # Tomar solo el nombre

        # Buscar el producto por nombre
        producto = next((p for p in self.productos if p["nombre"] == nombre_producto), None)
        if producto:
            self.preguntar_cantidad(producto)

        # Limpiar la barra de búsqueda
        self.searchBar.clear()

    def agregar_por_defecto(self):
        """Agregar al carrito con cantidad 1 si el usuario presiona Enter."""
        texto_busqueda = self.searchBar.text().lower()
        producto = next((p for p in self.productos if texto_busqueda in p["nombre"].lower()), None)
        if producto:
            self.preguntar_cantidad(producto)
            self.searchBar.clear()

    def mover_izquierda(self):
        self.scrollArea.horizontalScrollBar().setValue(
            self.scrollArea.horizontalScrollBar().value() - 100
        )

    def mover_derecha(self):
        self.scrollArea.horizontalScrollBar().setValue(
            self.scrollArea.horizontalScrollBar().value() + 100
        )

    def preguntar_cantidad(self, producto):
        cantidad, ok = QInputDialog.getInt(self, "Cantidad", f"Ingrese la cantidad para {producto['nombre']}:", 1, 1, 1000)
        if ok:
            self.agregar_al_carrito(producto, cantidad)

    def agregar_al_carrito(self, producto, cantidad):
        nueva_fila = self.cartTable.rowCount()
        self.cartTable.insertRow(nueva_fila)

        # Insertar datos en las celdas
        item_nombre = QTableWidgetItem(producto["nombre"])
        item_nombre.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # No editable
        self.cartTable.setItem(nueva_fila, 0, item_nombre)

        item_cantidad = QTableWidgetItem(str(cantidad))
        item_cantidad.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)  # Editable
        self.cartTable.setItem(nueva_fila, 1, item_cantidad)

        item_precio = QTableWidgetItem(f"${producto['precio']:.2f}")
        item_precio.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)  # No editable
        self.cartTable.setItem(nueva_fila, 2, item_precio)

        # Crear botón para eliminar producto
        botonEliminar = QPushButton()
        botonEliminar.setIcon(icon("fa.trash", color="red"))
        botonEliminar.setStyleSheet("border: none;")  # Estilo sin bordes
        botonEliminar.clicked.connect(lambda _, r=nueva_fila: self.eliminar_producto(r))
        self.cartTable.setCellWidget(nueva_fila, 3, botonEliminar)  # Añadir el botón en la columna 3

        self.actualizar_total()

    def eliminar_producto(self, row):
        self.cartTable.removeRow(row)
        self.actualizar_total()

    def actualizar_total(self):
        total = 0.0
        for row in range(self.cartTable.rowCount()):
            cantidad = int(self.cartTable.item(row, 1).text())
            precio = float(self.cartTable.item(row, 2).text().strip("$").replace(",", ""))
            total += cantidad * precio
        self.totalLabel.setText(f"Total: ${total:.2f}")