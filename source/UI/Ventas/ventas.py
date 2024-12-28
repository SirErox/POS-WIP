# Importaciones de PyQt5
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QHeaderView, QScrollArea, QWidget, QFrame, QMessageBox,
    QInputDialog, QTableWidgetItem, QListWidget
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QPoint

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
        self.searchBar.returnPressed.connect(self.agregar_por_defecto)
        self.leftSection.addWidget(self.searchBar)

        # Lista de sugerencias
        self.dropdownList = QListWidget(self)
        self.dropdownList.setWindowFlags(Qt.Popup)  # Ventana emergente
        self.dropdownList.hide()  # Ocultarla inicialmente
        self.dropdownList.activated.connect(self.seleccionar_producto)  # Conectar selección
        self.mainLayout.addWidget(self.dropdownList)

        # Tabla de carrito
        self.cartTable = QTableWidget()
        self.cartTable.setColumnCount(3)
        self.cartTable.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio"])
        self.cartTable.setFrameShape(QFrame.Box)
        self.cartTable.setObjectName("cartTable")
        self.cartTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # La columna de Producto será más ancha
        self.cartTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.cartTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.leftSection.addWidget(self.cartTable)

        # Barra inferior (carrusel)
        self.bottomBar = QWidget()
        self.bottomBar.setObjectName("bottomBar")
        self.bottomBarLayout = QVBoxLayout(self.bottomBar)

        # Área deslizante de productos
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedHeight(150)  # Reducir la altura del carrusel
        self.productContainer = QWidget()
        self.productLayout = QHBoxLayout(self.productContainer)
        self.scrollArea.setWidget(self.productContainer)
        self.bottomBarLayout.addWidget(self.scrollArea)

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
        self.bottomBarLayout.addLayout(self.navButtonsLayout)

        self.leftSection.addWidget(self.bottomBar)
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

        # Datos de productos
        self.productos = [
            {"nombre": "Producto 1", "imagen": "ruta/imagen1.jpg", "precio": 10.0},
            {"nombre": "Producto 2", "imagen": "ruta/imagen2.jpg", "precio": 15.0},
            {"nombre": "Producto 3", "imagen": "ruta/imagen3.jpg", "precio": 20.0},
            {"nombre": "Producto 4", "imagen": "ruta/imagen4.jpg", "precio": 25.0},
        ]

        self.mostrar_productos()

    def seleccionar_sugerencia(self, item):
        texto = item.text().split(" - ")[0]  # Obtener solo el nombre del producto
        self.searchBar.setText(texto)
        self.suggestionList.setVisible(False)  # Ocultar la lista después de seleccionar


    def finalizar_venta(self):  
        if self.cartTable.rowCount() == 0:
            QMessageBox.warning(self, "Carrito vacío", "No hay productos en el carrito.")
            return

        # Paso 1: Recopilar información del carrito
        items_carrito = []
        for row in range(self.cartTable.rowCount()):
            producto = self.cartTable.item(row, 0).text()
            cantidad = int(self.cartTable.item(row, 1).text())
            precio = float(self.cartTable.item(row, 2).text().strip("$").replace(",", ""))
            items_carrito.append({"nombre": producto, "cantidad": cantidad, "precio": precio})

        # Paso 2: Validar el stock de los productos
        for item in items_carrito:
            producto = self.app_manager.crud.obtener_producto_por_nombre(item["nombre"])
            if producto is None:
                QMessageBox.critical(self, "Error", f"El producto '{item['nombre']}' no existe en la base de datos.")
                return

            if producto.stock < item["cantidad"]:
                QMessageBox.warning(
                    self, 
                    "Stock insuficiente", 
                    f"El producto '{item['nombre']}' solo tiene {producto.stock} unidades disponibles."
                )
                return

        # Paso 3: Solicitar el método de pago
        metodos_pago = ["Efectivo", "Tarjeta", "Transferencia", "Otro"]
        metodo_pago, ok = QInputDialog.getItem(self, "Método de pago", "Seleccione un método de pago:", metodos_pago, editable=False)
        if not ok:
            return

        # Paso 4: Registrar la venta
        try:
            self.app_manager.crud.registrar_venta(
                usuario_id=self.usuario.id,  # ID del usuario logueado
                metodo_pago=metodo_pago,
                items=items_carrito
            )
            QMessageBox.information(self, "Venta registrada", "La venta se registró exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")

    def mostrar_productos(self):
        # Obtener productos desde la base de datos
        from source.database.database import SessionLocal
        from source.database.models import Inventario

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

        # Limpiar productos actuales
        for i in reversed(range(self.productLayout.count())):
            widget = self.productLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Mostrar productos cargados
        for producto in self.productos:
            frame = QWidget()
            frame.setFixedSize(100, 140)
            frameLayout = QVBoxLayout(frame)
            frameLayout.setContentsMargins(2, 2, 2, 2)

            # Imagen del producto
            imagen = QLabel()
            pixmap = QPixmap(producto["imagen"]).scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            imagen.setPixmap(pixmap)
            frameLayout.addWidget(imagen)

            # Nombre del producto
            nombre = QLabel(producto["nombre"])
            nombre.setAlignment(Qt.AlignCenter)
            nombre.setStyleSheet("font-size: 10pt;")
            nombre.setWordWrap(True)
            nombre.setFixedHeight(35)
            frameLayout.addWidget(nombre)

            # Botón para agregar al carrito
            botonAgregar = QPushButton("+")
            botonAgregar.setFixedSize(25, 25)
            botonAgregar.clicked.connect(lambda _, p=producto: self.preguntar_cantidad(p))
            frameLayout.addWidget(botonAgregar, alignment=Qt.AlignRight | Qt.AlignBottom)

            self.productLayout.addWidget(frame)

    def filtrar_productos(self):
        texto_busqueda = self.searchBar.text().lower()

        # Limpiar la lista desplegable
        self.dropdownList.clear()

        # Filtrar productos que coincidan con el texto de búsqueda
        productos_filtrados = [
            producto for producto in self.productos
            if texto_busqueda in producto["nombre"].lower()
        ]

        # Limpiar la lista desplegable
        self.dropdownList.clear()

        if productos_filtrados:
            # Agregar productos filtrados a la lista desplegable
            for producto in productos_filtrados:
                self.dropdownList.addItem(f"{producto['nombre']} - ${producto['precio']:.2f}")
        
            # Mostrar y posicionar la lista debajo de la barra de búsqueda
            self.posicionar_lista()
            self.dropdownList.show()
        else:
            # Ocultar la lista si no hay resultados
            self.dropdownList.hide()

    def posicionar_lista(self):
        """Posicionar la lista desplegable debajo de la barra de búsqueda."""
        pos = self.searchBar.mapToGlobal(QPoint(0, self.searchBar.height()))
        self.dropdownList.move(pos)
        self.dropdownList.setFixedWidth(self.searchBar.width())

    def actualizar_lista(self):
        """Actualizar la lista desplegable según el texto de búsqueda."""
        texto_busqueda = self.searchBar.text().lower()
        productos_filtrados = [
            producto for producto in self.productos
            if texto_busqueda in producto["nombre"].lower()
        ]

        # Limpiar y ocultar lista si no hay resultados
        self.dropdownList.clear()
        if not productos_filtrados:
            self.dropdownList.hide()
            return

        # Agregar productos filtrados a la lista desplegable
        for producto in productos_filtrados:
            self.dropdownList.addItem(f"{producto['nombre']} - ${producto['precio']:.2f}")

        # Mostrar la lista desplegable
        self.dropdownList.show()
    

    def seleccionar_producto(self, index):
        """Agregar el producto seleccionado desde la lista desplegable."""
        if index < 0:
            return  # Si no hay selección válida, salir

        # Obtener el producto seleccionado
        producto_texto = self.dropdownList.itemText(index)
        nombre_producto = producto_texto.split(" - ")[0]

        # Buscar el producto por nombre
        producto = next((p for p in self.productos if p["nombre"] == nombre_producto), None)
        if producto:
            self.preguntar_cantidad(producto)

        # Ocultar la lista y limpiar la barra de búsqueda
        self.dropdownList.hide()
        self.searchBar.clear()

    def agregar_por_defecto(self):
        """Agregar al carrito con cantidad 1 si el usuario presiona Enter."""
        texto_busqueda = self.searchBar.text().lower()
        producto = next((p for p in self.productos if texto_busqueda in p["nombre"].lower()), None)
        if producto:
            self.agregar_al_carrito(producto, 1)
            self.searchBar.clear()
            self.dropdownList.hide()

    def mover_izquierda(self):
        self.scrollArea.horizontalScrollBar().setValue(
            self.scrollArea.horizontalScrollBar().value() - 100
        )

    def mover_derecha(self):
        self.scrollArea.horizontalScrollBar().setValue(
            self.scrollArea.horizontalScrollBar().value() + 100
        )

    def preguntar_cantidad(self, producto):
        cantidad, ok = QInputDialog.getInt(self, "Agregar al carrito", f"Cantidad de {producto['nombre']}:", min=1, value=1)
        if ok:
            self.agregar_al_carrito(producto, cantidad)

    def agregar_al_carrito(self, producto, cantidad):
        # Buscar si ya está en el carrito
        for row in range(self.cartTable.rowCount()):
            if self.cartTable.item(row, 0).text() == producto["nombre"]:
                cantidad_actual = int(self.cartTable.item(row, 1).text())
                self.cartTable.setItem(row, 1, QTableWidgetItem(str(cantidad_actual + cantidad)))
                self.actualizar_total()
                return

        # Si no está, agregar nueva fila
        row_position = self.cartTable.rowCount()
        self.cartTable.insertRow(row_position)
        self.cartTable.setItem(row_position, 0, QTableWidgetItem(producto["nombre"]))
        self.cartTable.setItem(row_position, 1, QTableWidgetItem(str(cantidad)))
        self.cartTable.setItem(row_position, 2, QTableWidgetItem(f"${producto['precio']:.2f}"))
        self.actualizar_total()

    def actualizar_total(self):
        total = 0.0
        for row in range(self.cartTable.rowCount()):
            cantidad = int(self.cartTable.item(row, 1).text())
            precio = float(self.cartTable.item(row, 2).text().strip("$").replace(",", ""))
            total += cantidad * precio
        self.totalLabel.setText(f"Total: ${total:.2f}")
