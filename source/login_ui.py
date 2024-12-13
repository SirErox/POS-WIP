from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from .crud import listar_usuarios  # Importar la función para validar usuarios
from .security import verificar_contra,hashear_contra
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
         #para quitar el icono de la ventana
        #self.setWindowIcon(QtGui.QIcon(None))
        self.setWindowTitle("Login - POS System")
        self.setFixedSize(200, 150)
        self.setStyleSheet(open('source/styles/login.css').read())
        # Layout y widgets
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.label_user = QLabel("Usuario:")
        self.input_user = QLineEdit()
        self.label_pass = QLabel("Contraseña:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)  # Ocultar la contraseña

        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.validate_login)

        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # Resultado de la autenticación
        self.authenticated = False

        # Conectar el botón de login
        self.login_button.clicked.connect(self.validate_login)

    def validate_login(self):
        username = self.input_user.text()
        password = self.input_pass.text()
        hpassword = hashear_contra(password)
        # Validar usuario con la base de datos
        usuarios = listar_usuarios()
        for usuario in usuarios:
            if usuario.username == username and usuario.password == password:
                QMessageBox.information(self, "Login", f"Bienvenido {usuario.nombre}")
                self.authenticated = True
                self.accept()  # Cierra el diálogo
                return
            else:
                # Si no se encontró el usuario
                QMessageBox.warning(self, "Login", "Credenciales incorrectas. Inténtalo de nuevo.")
