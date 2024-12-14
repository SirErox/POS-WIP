from PyQt5.QtWidgets import (QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog, QMessageBox,
                             QWidget,QSpacerItem,QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap
from ..crud import listar_usuarios  # Importar la función para validar usuarios
from ..security import verificar_contra
from ..UI.main_window import MainWindow
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - POS System")
        self.setGeometry(500,200,200, 150)
        #para quitar el icono de la ventana
        self.setWindowIcon(QIcon(None))
        #quitar icono ? de la ventana
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # Cargar estilos
        try:
            with open('source/styles/login.css', 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Archivo de estilo no encontrado: login.css")

        self.init_ui()

    def init_ui(self):
        # Layout y widgets
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Logo
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("source/icons/logo.jpeg").scaled(200, 250, Qt.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignCenter)

         # Espacio entre logo y campos de texto
        layout.addWidget(self.logo_label)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.label_user = QLabel("Usuario:")
        self.input_user = QLineEdit(self)
        self.input_user.setPlaceholderText("Usuario")
        self.label_pass = QLabel("Contraseña:")
        self.input_pass = QLineEdit(self)
        self.input_pass.setPlaceholderText("contraseña")
        self.input_pass.setEchoMode(QLineEdit.Password)  # Ocultar la contraseña

        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.validate_login)

        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.login_button)
        # Espaciador final
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

        # Resultado de la autenticación
        self.authenticated = False
        self.usuario=None

    def validate_login(self):
        username = self.input_user.text()
        password = self.input_pass.text()     
        # Validar usuario con la base de datos
        usuarios = listar_usuarios()
        for usuario in usuarios:
            if usuario.username == username and verificar_contra(password,usuario.password):
                QMessageBox.information(self, "Login", f"Bienvenido {usuario.nombre}")
                self.authenticated = True
                self.usuario=usuario
                self.accept()  # Cierra el diálogo
                # Abrir ventana principal
                main_window = MainWindow(usuario)
                main_window.show()
                return
            else:
                # Si no se encontró el usuariox
                QMessageBox.warning(self, "Login", "Credenciales incorrectas. Inténtalo de nuevo.")
