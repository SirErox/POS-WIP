from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton

class UserFormDialog(QDialog):
    """Diálogo personalizado para Añadir o Editar un usuario."""

    def __init__(self, title, nombre="", username="", rol="", password=""):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(450, 250, 300, 250)

        layout = QVBoxLayout()

        # Campos del formulario
        layout.addWidget(QLabel("Nombre:"))
        self.name_input = QLineEdit(nombre)
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit(username)
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Contraseña:"))
        self.password_input = QLineEdit(password)
        self.password_input.setEchoMode(QLineEdit.Password)  # Ocultar el texto
        layout.addWidget(self.password_input)

        layout.addWidget(QLabel("Rol:"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Administrador", "Cajero", "Supervisor"])  # Roles predefinidos
        self.role_combo.setCurrentText(rol)
        layout.addWidget(self.role_combo)

        # Botón OK
        self.ok_button = QPushButton("Aceptar")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_data(self):
        """Retorna los valores del formulario."""
        return (
            self.name_input.text(),
            self.username_input.text(),
            self.password_input.text(),
            self.role_combo.currentText(),
        )

