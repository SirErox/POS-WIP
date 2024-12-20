from PyQt5.QtWidgets import (QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog, QMessageBox,
                             QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from source.database.crud import listar_usuarios  # Importar la función para validar usuarios
from source.database.security import verificar_contra
from source.Utils.auditoria import registrar_accion
from source.database.database import SessionLocal
from source.database.models import Table_usuario as Usuario


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - POS System")
        self.setGeometry(500, 100, 200, 150)  # Ajustar tamaño de la ventana
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

        # Layout principal
        layout = QVBoxLayout(self)

        # Logo
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("source/icons/logo.jpeg").scaled(250, 300, Qt.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Campos de usuario y contraseña
        self.usuario_label = QLabel("Usuario:")
        self.usuario_input = QLineEdit()
        self.contrasena_label = QLabel("Contraseña:")
        self.contrasena_input = QLineEdit()
        self.contrasena_input.setEchoMode(QLineEdit.Password)

        # Botón de inicio de sesión
        self.boton_iniciar_sesion = QPushButton("Iniciar Sesión")
        self.boton_iniciar_sesion.clicked.connect(self.iniciar_sesion)

        # Añadir elementos al layout
        layout.addWidget(self.usuario_label)
        layout.addWidget(self.usuario_input)
        layout.addWidget(self.contrasena_label)
        layout.addWidget(self.contrasena_input)
        layout.addWidget(self.boton_iniciar_sesion)

        self.setLayout(layout)

    def iniciar_sesion(self):
        """Manejador para el inicio de sesión."""
        usuario = self.usuario_input.text()
        contrasena = self.contrasena_input.text()

        # Validar credenciales
        with SessionLocal() as session:
            try:
                usuario_obj = session.query(Usuario).filter(Usuario.username == usuario).first()
                if usuario_obj and verificar_contra(contrasena, usuario_obj.password):
                    # Registrar acción de inicio de sesión
                    registrar_accion(usuario_obj.id, "Inicio de Sesión", f"El usuario {usuario} ha iniciado sesión.")
                    QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso.")
                    self.usuario = usuario_obj  # Guardar el usuario en la clase
                    self.accept()  # Notificar que el login fue exitoso
                else:
                    QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al iniciar sesión: {e}")
                raise e
