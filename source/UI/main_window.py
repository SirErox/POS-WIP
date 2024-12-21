from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import qtawesome as qta
from .user_control import UserControlWindow
from .inventario.inv_control import VentanaInventario
from source.Utils.auditoria import registrar_accion  # Importar la función para registrar acciones

class MainWindow(QMainWindow):
    def __init__(self, app_manager, usuario):
        super().__init__()
        self.app_manager = app_manager
        self.usuario = usuario
        self.setWindowTitle("PANEL PRINCIPAL - Bienvenido " + self.usuario.username)
        self.resize(1280, 720)

        # Layout principal
        main_layout = QHBoxLayout()

        # Menú lateral derecho
        self.menu_layout = QVBoxLayout()
        self.menu_layout.setAlignment(Qt.AlignTop)
        self.menu_widget = QWidget()
        self.menu_widget.setObjectName("menu_widget")
        self.menu_widget.setLayout(self.menu_layout)
        self.menu_width_collapsed = 60
        self.menu_width_expanded = 200
        self.menu_widget.setFixedWidth(self.menu_width_expanded)
        # Logo
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("source/icons/logo.jpeg").scaled(150, 150, Qt.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.menu_layout.addWidget(self.logo_label)

        # Botones del menú
        self.add_menu_button("Inventario", 'fa.cubes', self.abrir_inventario)
        self.add_menu_button("Usuarios", 'fa.users', self.abrir_usuarios)
        self.add_menu_button("Ventas", 'fa.line-chart', self.abrir_ventas)

        # Botón de cerrar sesión
        logout_button = QPushButton("Cerrar Sesión")
        logout_button.setObjectName("logout_button")
        logout_button.setIcon(qta.icon('fa.sign-out'))
        logout_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        logout_button.clicked.connect(self.cerrar_sesion)  # Acción de cierre temporal
        self.menu_layout.addStretch()
        self.menu_layout.addWidget(logout_button)

        # Espacio central
        self.content_widget = QWidget()
        self.content_widget.setObjectName("content_widget")

        # Agregar al layout principal
        main_layout.addWidget(self.content_widget)
        main_layout.addWidget(self.menu_widget)

        # Toggle para colapsar el menú
        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(qta.icon('fa.arrow-right'))
        self.toggle_button.setFixedSize(30, 30)
        self.toggle_button.clicked.connect(self.toggle_menu)
        self.menu_layout.insertWidget(0, self.toggle_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Cargar Estilos
        self.cargar_estilos()

    def add_menu_button(self, text, icon_name, callback):
        """Crea un botón con ícono y texto para el menú."""
        button = QPushButton(text)
        button.setIcon(qta.icon(icon_name))
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button.clicked.connect(callback)
        self.menu_layout.addWidget(button)

    def toggle_menu(self):
        """Colapsa o expande el menú lateral."""
        current_width = self.menu_widget.width()
        if current_width == self.menu_width_expanded:
            # Colapsar menú
            self.menu_widget.setFixedWidth(self.menu_width_collapsed)
            self.toggle_button.setIcon(qta.icon('fa.arrow-left'))
            self.logo_label.hide()  # Ocultar el logo al colapsar
            for i in range(self.menu_layout.count()):
                item = self.menu_layout.itemAt(i).widget()
                if isinstance(item, QPushButton) and item is not self.toggle_button:
                    item.setProperty('originalText', item.text())
                    item.setText("")  # Ocultar el texto de los botones
        else:
            # Expandir menú
            self.menu_widget.setFixedWidth(self.menu_width_expanded)
            self.toggle_button.setIcon(qta.icon('fa.arrow-left'))
            self.logo_label.show()  # Mostrar el logo al expandir
            for i in range(self.menu_layout.count()):
                item = self.menu_layout.itemAt(i).widget()
                if isinstance(item, QPushButton) and item is not self.toggle_button:
                    item.setText(item.property('originalText'))  # Mostrar el texto de los botones


    def cargar_estilos(self):
        try:
            with open('source/styles/styles.css', 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Archivo de estilo no encontrado: styles.css")
        except Exception as e:
            print(f"Error al cargar la hoja de estilos: {e}")

    def abrir_inventario(self):
        """Abre la ventana de inventario."""
        self.inv_window = VentanaInventario(self.usuario.id)
        self.inv_window.show()

    def abrir_usuarios(self):
        """Abre la ventana de usuarios."""
        self.user_window = UserControlWindow(self.usuario.id)
        self.user_window.show()

    def abrir_ventas(self):
        """Abre la ventana de ventas."""
        print("Abrir Ventas")
        # Aquí puedes abrir la ventana de ventas

    def cerrar_sesion(self):
        """Cierra la sesión y regresa a la ventana de login."""
        registrar_accion(self.usuario.id, "Cierre de Sesión", f"El usuario {self.usuario.username} ha cerrado sesión.")
        self.app_manager.mostrar_login()
