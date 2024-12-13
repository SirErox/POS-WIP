from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from ..crud import listar_usuarios  # Importar la función para validar usuarios
from ..security import verificar_contra
from ..UI.main_window import MainWindow
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
         #para quitar el icono de la ventana
        #self.setWindowIcon()
        self.setWindowTitle("Login - POS System")
        self.setFixedSize(200, 150)
        
        # Cargar estilos
        try:
            with open('source/styles/login.css', 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Archivo de estilo no encontrado: login.css")

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

    def validate_login(self):
        username = self.input_user.text()
        password = self.input_pass.text()     
        # Validar usuario con la base de datos
        usuarios = listar_usuarios()
        for usuario in usuarios:
            if usuario.username == username and verificar_contra(password,usuario.password):
                QMessageBox.information(self, "Login", f"Bienvenido {usuario.nombre}")
                self.authenticated = True
                self.accept()  # Cierra el diálogo
                # Abrir ventana principal
                main_window = MainWindow(usuario)
                main_window.show()
                return
            else:
                # Si no se encontró el usuariox
                QMessageBox.warning(self, "Login", "Credenciales incorrectas. Inténtalo de nuevo.")
