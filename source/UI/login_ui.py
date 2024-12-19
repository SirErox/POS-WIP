from PyQt5.QtWidgets import (QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog, QMessageBox,
                             QSpacerItem, QSizePolicy, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ..database.crud import listar_usuarios  # Importar la función para validar usuarios
from ..database.security import verificar_contra
from ..UI.main_window import MainWindow
from source.Utils.auditoria import registrar_accion
from source.database.database import SessionLocal
from source.database.models import Table_usuario as Usuario

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - POS System")
        self.setGeometry(500, 100, 200, 150)  # Ajustar el tamaño de la ventana
        # Quitar icono ? de la ventana
        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        # Cargar estilos
        try:
            with open('source/styles/login.css', 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            pass

        layout = QVBoxLayout(self)

        # Añadir imagen del logo con medidas ajustadas
        # Logo
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("source/icons/logo.jpeg").scaled(250, 300, Qt.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        self.usuario_label = QLabel("Usuario:")
        self.usuario_input = QLineEdit()
        self.contrasena_label = QLabel("Contraseña:")
        self.contrasena_input = QLineEdit()
        self.contrasena_input.setEchoMode(QLineEdit.Password)

        self.boton_iniciar_sesion = QPushButton("Iniciar Sesión")
        self.boton_iniciar_sesion.clicked.connect(self.iniciar_sesion)

        layout.addWidget(self.usuario_label)
        layout.addWidget(self.usuario_input)
        layout.addWidget(self.contrasena_label)
        layout.addWidget(self.contrasena_input)
        layout.addWidget(self.boton_iniciar_sesion)

        self.setLayout(layout)

    def iniciar_sesion(self):
        usuario = self.usuario_input.text()
        contrasena = self.contrasena_input.text()

        session = SessionLocal()
        try:
            usuario_obj = session.query(Usuario).filter(Usuario.username == usuario).first()
            if usuario_obj and verificar_contra(contrasena, usuario_obj.password):
                # Registrar acción de inicio de sesión
                registrar_accion(usuario_obj.id, "Inicio de Sesión", f"El usuario {usuario} ha iniciado sesión.")
                QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso.")
                self.usuario = usuario_obj  # Definir el atributo usuario
                self.accept()
                # Abrir la ventana principal pasando el usuario
                self.main_window = MainWindow(self.usuario)
                self.main_window.show()
            else:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar sesión: {e}")
            raise e
        finally:
            session.close()
