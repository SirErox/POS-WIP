from PyQt5.QtWidgets import(  QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QFormLayout, QDateEdit, QComboBox, QSpinBox)
from PyQt5.QtCore import QDate
class UserFormDialog(QWidget):
    """Diálogo personalizado para Añadir o Editar un usuario."""
    def __init__(self,user_data=None):
        super().__init__(parent)
        self.setWindowTitle("Formulario de usuario")
        self.setFixedSize(400,500)
        self.user_data=user_data
        self.photo_path=""

        self.init_ui()
        if user_data:
            self.populate_form(user_data)

    def init_ui(self):
        layout = QVBoxLayout()
        # Formulario
        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.fullname_input = QLineEdit()
        self.role_input = QComboBox()
        self.role_input.addItems(["Administrador", "Cajero"])

        self.status_input = QComboBox()
        self.status_input.addItems(["Activo", "Inactivo"])

        self.antiguedad_input = QLineEdit()
        self.last_editor_input = QLineEdit()
        self.last_editor_input.setReadOnly(True)

        # Campo de Foto
        self.photo_label = QLabel("Sin foto")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setFixedSize(100, 100)
        self.photo_label.setStyleSheet("border: 1px solid gray;")
        upload_button = QPushButton("Cargar Foto")
        upload_button.clicked.connect(self.upload_photo)

        photo_layout = QHBoxLayout()
        photo_layout.addWidget(self.photo_label)
        photo_layout.addWidget(upload_button)

        # Agregar campos al formulario
        form_layout.addRow("Usuario:", self.username_input)
        form_layout.addRow("Nombre Completo:", self.fullname_input)
        form_layout.addRow("Rol:", self.role_input)
        form_layout.addRow("Estado:", self.status_input)
        form_layout.addRow("Antigüedad (años):", self.antiguedad_input)
        form_layout.addRow("Último Editor:", self.last_editor_input)
        form_layout.addRow("Foto:", photo_layout)

        layout.addLayout(form_layout)

        # Botones
        button_layout = QHBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_user)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def upload_photo(self):
        """Subir una foto y mostrarla."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.photo_path = file_path
            pixmap = QPixmap(file_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_label.setPixmap(pixmap)

    def populate_form(self, user_data):
        """Llenar el formulario con datos existentes."""
        self.username_input.setText(user_data['username'])
        self.fullname_input.setText(user_data['nombre_completo'])
        self.role_input.setCurrentText(user_data['rol'])
        self.status_input.setCurrentText(user_data['estado'])
        self.antiguedad_input.setText(str(user_data['antiguedad']))
        self.last_editor_input.setText(user_data['ultimo_editor'])
        if user_data['foto']:
            self.photo_path = user_data['foto']
            pixmap = QPixmap(self.photo_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_label.setPixmap(pixmap)

    def save_user(self):
        """Guardar usuario (datos a la base de datos)."""
        user_info = {
            "username": self.username_input.text(),
            "nombre_completo": self.fullname_input.text(),
            "rol": self.role_input.currentText(),
            "estado": self.status_input.currentText(),
            "antiguedad": self.antiguedad_input.text(),
            "ultimo_editor": self.last_editor_input.text(),
            "foto": self.photo_path
        }
        print("Usuario Guardado:", user_info)  # Aquí iría la lógica para guardar en la base de datos
        self.accept()