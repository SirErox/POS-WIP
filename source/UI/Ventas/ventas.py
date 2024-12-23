import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QScrollArea, QFrame, QMessageBox, QSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

class VentasWindow(QMainWindow):
    def __init__(self,usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("VENTAS")
        self.setWindowIcon(QIcon('source/icons/logo.jpeg'))
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        main_layout = QVBoxLayout()

        # Barra inferior
        self.bar_inferior = self.create_bar_inferior()
        main_layout.addWidget(self.bar_inferior)

        # Widget principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_bar_inferior(self):
        # Contenedor principal
        bar_container = QFrame()
        bar_container.setFrameShape(QFrame.StyledPanel)
        bar_container.setFixedHeight(200)

        bar_layout = QVBoxLayout()

        # Barra de búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar producto...")
        self.search_input.textChanged.connect(self.filter_products)

        search_layout.addWidget(QLabel("Buscar:"))
        search_layout.addWidget(self.search_input)

        bar_layout.addLayout(search_layout)

        # Carrusel de productos
        scroll_area = QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)

        self.product_container = QFrame()
        self.product_layout = QHBoxLayout()
        self.product_container.setLayout(self.product_layout)

        scroll_area.setWidget(self.product_container)

        bar_layout.addWidget(scroll_area)

        # Configurar el layout principal
        bar_container.setLayout(bar_layout)

        # Añadir productos de ejemplo
        self.load_products()

        return bar_container

    def load_products(self):
        # Ejemplo de productos
        products = [
            {"name": "Producto 1", "price": 10.0, "image": "placeholder.png"},
            {"name": "Producto 2", "price": 15.0, "image": "placeholder.png"},
            {"name": "Producto 3", "price": 20.0, "image": "placeholder.png"},
        ]

        for product in products:
            self.add_product_to_bar(product)

    def add_product_to_bar(self, product):
        # Contenedor de producto
        product_frame = QFrame()
        product_frame.setFrameShape(QFrame.StyledPanel)
        product_frame.setFixedSize(100, 100)

        product_layout = QVBoxLayout()

        # Imagen del producto
        product_image = QLabel()
        pixmap = QPixmap(product["image"]).scaled(100, 100, Qt.KeepAspectRatio)
        product_image.setPixmap(pixmap)
        product_image.setAlignment(Qt.AlignCenter)
        product_layout.addWidget(product_image)

        # Nombre del producto
        product_name = QLabel(product["name"])
        product_name.setAlignment(Qt.AlignCenter)
        product_layout.addWidget(product_name)

        # Precio del producto
        product_price = QLabel(f"${product['price']:.2f}")
        product_price.setAlignment(Qt.AlignCenter)
        product_layout.addWidget(product_price)

        # Botón para añadir al carrito
        add_button = QPushButton("+")
        add_button.clicked.connect(lambda: self.add_to_cart(product))
        product_layout.addWidget(add_button)

        product_frame.setLayout(product_layout)
        self.product_layout.addWidget(product_frame)

    def filter_products(self):
        # Filtrar productos según el texto de búsqueda
        search_text = self.search_input.text().lower()
        for i in range(self.product_layout.count()):
            product_widget = self.product_layout.itemAt(i).widget()
            if product_widget:
                product_name = product_widget.findChild(QLabel).text().lower()
                product_widget.setVisible(search_text in product_name)

    def add_to_cart(self, product):
        # Ventana para seleccionar la cantidad
        cantidad, ok = self.show_quantity_dialog(product["name"])
        if ok:
            QMessageBox.information(self, "Carrito", f"Añadido {cantidad} de {product['name']} al carrito.")

    def show_quantity_dialog(self, product_name):
        # Cuadro emergente para ingresar cantidad
        dialog = QFrame(self)
        dialog.setWindowTitle(f"Cantidad para {product_name}")
        dialog_layout = QVBoxLayout()

        label = QLabel("Ingrese la cantidad:")
        spin_box = QSpinBox()
        spin_box.setRange(1, 999)
        spin_box.setValue(1)

        confirm_button = QPushButton("Aceptar")
        confirm_button.clicked.connect(lambda: dialog.close())

        dialog_layout.addWidget(label)
        dialog_layout.addWidget(spin_box)
        dialog_layout.addWidget(confirm_button)
        dialog.setLayout(dialog_layout)

        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

        return spin_box.value(), True
