from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QMessageBox,
    QInputDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from database import SessionLocal
from .User_form import UserFormDialog
from ..crud import agregar_usuario,eliminar_usuario,editar_usuario,listar_usuarios
class UserControlWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Usuarios")
        self.setGeometry(400, 200, 800, 500)
        self.setWindowIcon(QIcon('source/icons/users.png'))
        # Cargar estilos desde main.css
        self.load_styles("main.css")
        self.session=SessionLocal()
        # Inicializar UI
        self.init_ui()
        self.load_users()  # Cargar usuarios al abrir la ventana

    def load_styles(self, css_file):
        """Cargar hoja de estilos externa."""
        try:
            with open('source/styles/main.css', 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Archivo de estilo no encontrado: main.css")

    def init_ui(self):
        """Interfaz principal."""
        main_layout = QVBoxLayout()

        # Título
        title = QLabel("Control de Usuarios")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("titleLabel")  # Vincular a main.css
        main_layout.addWidget(title)

        # Tabla de usuarios
        self.user_table = QTableWidget(0, 3)  # 3 columnas
        self.user_table.setHorizontalHeaderLabels(["ID", "Usuario", "Rol"])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.user_table)

        # Botones
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Añadir Usuario")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_user)

        self.edit_button = QPushButton("Editar Usuario")
        self.edit_button.setObjectName("editButton")
        self.edit_button.clicked.connect(self.edit_user)

        self.delete_button = QPushButton("Eliminar Usuario")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(self.delete_user)

        self.exit_button = QPushButton("Salir")
        self.exit_button.setObjectName("exitButton")
        self.exit_button.clicked.connect(self.close)

        # Agregar botones al layout
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.exit_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def load_users(self):
        """Cargar datos de usuarios desde la base de datos."""
        try:
            users = listar_usuarios()  # Llama al CRUD
            self.user_table.setRowCount(len(users))
            for row_idx, user in enumerate(users):
                self.user_table.setItem(row_idx, 0, QTableWidgetItem(str(user.id)))
                self.user_table.setItem(row_idx, 1, QTableWidgetItem(user.nombre))
                self.user_table.setItem(row_idx, 2, QTableWidgetItem(user.rol))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los usuarios: {e}")
    
    def add_user(self):
        """Función para añadir usuario."""
        dialog = UserFormDialog("Añadir Usuario")
        if dialog.exec_():  # Si el usuario presiona "Aceptar"
            nombre, username, password, rol = dialog.get_data()
            if nombre and username and password and rol:
                try:
                    agregar_usuario(nombre, username, password, rol)  # Contraseña temporal
                    QMessageBox.information(self, "Éxito", "Usuario agregado correctamente.")
                    self.load_users()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo agregar el usuario: {e}")
            else:
                QMessageBox.warning(self, "Atención", "Todos los campos son obligatorios.")

    def edit_user(self):
        """Función para editar usuario."""
        selected = self.user_table.currentRow()
        if selected >= 0:
            user_id = int(self.user_table.item(selected, 0).text())
            current_nombre = self.user_table.item(selected, 1).text()
            current_rol = self.user_table.item(selected, 2).text()

            # Obtener datos actuales (contraseña se pide de nuevo por seguridad)
            dialog = UserFormDialog(
                "Editar Usuario", 
                nombre=current_nombre, 
                rol=current_rol
            )
            if dialog.exec_():
                new_nombre, new_username, new_password, new_rol = dialog.get_data()
                if new_nombre and new_username and new_rol:
                    try:
                        editar_usuario(user_id, new_nombre, new_username, new_password, new_rol)
                        QMessageBox.information(self, "Éxito", "Usuario editado correctamente.")
                        self.load_users()
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"No se pudo editar el usuario: {e}")
                else:
                    QMessageBox.warning(self, "Atención", "Todos los campos son obligatorios.")
        else:
            QMessageBox.warning(self, "Atención", "Seleccione un usuario para editar.")

    def delete_user(self):
        """Función para eliminar usuario."""
        selected = self.user_table.currentRow()
        if selected >= 0:
            user_id = int(self.user_table.item(selected, 0).text())
            confirmation = QMessageBox.question(
                self, "Eliminar Usuario", f"¿Seguro que quieres eliminar el usuario ID {user_id}?",
                QMessageBox.Yes | QMessageBox.No
            )
        if confirmation == QMessageBox.Yes:
            try:
                eliminar_usuario(user_id)  # Llamada a la función CRUD
                QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente.")
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el usuario: {e}")
        else:
            QMessageBox.warning(self, "Atención", "Seleccione un usuario para eliminar.")

