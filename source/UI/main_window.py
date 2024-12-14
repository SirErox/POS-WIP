from PyQt5.QtWidgets import(QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QMessageBox,
                            QStackedWidget,QHBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QPropertyAnimation,QSize
from .user_control import UserControlWindow
class MainWindow(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"POS - Bienvenido {self.usuario.nombre}")
        self.setWindowIcon(QIcon('source/icons/logo.ico'))  
        self.resize(800, 600)

        # Layout Principal
        self.main_layout = QHBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Menú lateral y contenido
        self.menu_expanded = False  # Estado del menú
        self.setup_menu()
        self.setup_pages()

    def setup_menu(self):
        # Menú lateral
        self.menu_widget = QWidget()
        self.menu_widget.setFixedWidth(60)  # Anchura inicial del menú colapsado
        self.menu_widget.setStyleSheet("background-color: #2c3e50; color: white;")

        # Layout del menú
        self.menu_layout = QVBoxLayout()
        self.menu_widget.setLayout(self.menu_layout)
        self.menu_layout.setAlignment(Qt.AlignTop)

        # Botón de hamburguesa
        self.hamburger_button = QPushButton()
        self.hamburger_button.setIcon(QIcon('source/icons/menu.png'))  # Ícono de menú hamburguesa
        self.hamburger_button.setIconSize(QSize(32, 32))
        self.hamburger_button.setStyleSheet("border: none;")
        self.hamburger_button.clicked.connect(self.toggle_menu)
        self.menu_layout.addWidget(self.hamburger_button)

        # Botones del menú
        self.buttons = {}
        self.add_menu_button("Inicio", 'source/icons/home.png', self.show_inicio)
        self.add_menu_button("Ventas", 'source/icons/sales.png', self.show_ventas)

        if self.usuario.rol == "administrador":
            self.add_menu_button("Control de Usuarios", 'source/icons/users.png', self.open_user_control)

        # Menú expandible
        self.menu_expanded = False
        self.animation = QPropertyAnimation(self.menu_widget, b"maximumWidth")
        self.animation.setDuration(300)

        self.main_layout.addWidget(self.menu_widget)
        
    def add_menu_button(self, name,icon_path, callback):
         # Botón con icono y texto
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(24, 24))
        button.setText(name)
        button.setStyleSheet("""
            QPushButton {
                background-color: #34495e; 
                color: white; 
                border: none; 
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
        """)
        button.clicked.connect(callback)
        button.setCheckable(True)
        button.setVisible(True)  # Botón siempre visible
        self.menu_layout.addWidget(button)
        self.buttons[name] = button
    
    def toggle_menu(self):
        # Expande o colapsa el menú
        if self.menu_expanded:
            self.animation.setStartValue(200)  # Expandido
            self.animation.setEndValue(60)    # Colapsado
            self.update_button_view(False)
        else:
            self.animation.setStartValue(60)  # Colapsado
            self.animation.setEndValue(200)   # Expandido
            self.update_button_view(True)

        self.animation.start()
        self.menu_expanded = not self.menu_expanded
    
    def setup_pages(self):
        # Contenedor de páginas
        self.pages = QStackedWidget()
       # Contenedor de páginas
        self.pages = QStackedWidget()
        self.main_layout.addWidget(self.pages)

        # Página Inicio
        self.page_inicio = QLabel("Bienvenido al sistema POS")
        self.page_inicio.setAlignment(Qt.AlignCenter)
        self.pages.addWidget(self.page_inicio)

        # Página Ventas
        self.page_ventas = QLabel("Página de Ventas")
        self.page_ventas.setAlignment(Qt.AlignCenter)
        self.pages.addWidget(self.page_ventas)

        # Página Control de Usuarios
        self.page_user_control = QLabel("Control de Usuarios")
        self.page_user_control.setAlignment(Qt.AlignCenter)
        self.pages.addWidget(self.page_user_control)

        # Configuración inicial
        self.show_inicio()

    def update_button_view(self, expanded):
        for name, button in self.buttons.items():
            if expanded:
                button.setText(name)  # Muestra texto
                button.setIconSize(QSize(0,0))  # ocultamos el icono
            else:
                button.setText("")  # ocultamos el texxto
                button.setIconSize(QSize(24,24))

    def show_inicio(self):
        self.update_menu_selection("Inicio")
        self.pages.setCurrentWidget(self.page_inicio)

    def show_ventas(self):
        self.update_menu_selection("Ventas")
        self.pages.setCurrentWidget(self.page_ventas)

    def show_user_control(self):
        self.update_menu_selection("Control de Usuarios")
        self.pages.setCurrentWidget(self.page_user_control)

    def update_menu_selection(self, selected_name):
        for name, button in self.buttons.items():
            button.setChecked(name == selected_name)

    def open_user_control(self):
        user_control_window=UserControlWindow()
        user_control_window.show()

    def abrir_ventana_ventas(self):
        QMessageBox.information(self, "Ventas", "Abriendo la ventana de ventas...")

    def abrir_gestion_inventario(self):
        QMessageBox.information(self, "Gestión de Inventario", "Abriendo la gestión de inventario...")

