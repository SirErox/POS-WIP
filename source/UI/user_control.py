from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap
from database import SessionLocal
from .User_form import UserFormDialog
from ..database.crud import agregar_usuario,eliminar_usuario,editar_usuario,listar_usuarios
class UserControlWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Usuarios")
        self.setGeometry(400, 200, 1000, 600)
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
        self.user_table = QTableWidget(0, 8)  # 3 columnas
        self.user_table.setHorizontalHeaderLabels(["ID", "Usuario", "Nombre Completo", "Rol", "Estado", "Antigüedad", "Último Editor", "Foto"])

        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Bloquear edición
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setAlternatingRowColors(True)
        main_layout.addWidget(self.user_table)

        # Ajustar tamaño de columnas
        self.user_table.setColumnWidth(0, 50)   # ID
        self.user_table.setColumnWidth(1, 100)  # Usuario
        self.user_table.setColumnWidth(2, 200)  # Nombre Completo
        self.user_table.setColumnWidth(3, 120)  # Rol
        self.user_table.setColumnWidth(4, 80)   # Estado
        self.user_table.setColumnWidth(5, 100)  # Antigüedad
        self.user_table.setColumnWidth(6, 120)  # Último Editor
        self.user_table.setColumnWidth(7, 80)   # Foto

        # Botones
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Añadir Usuario")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(lambda: self.add_user())

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
            users = listar_usuarios()
            self.user_table.setRowCount(len(users))
            for row_idx, user in enumerate(users):
                self.user_table.setItem(row_idx, 0, QTableWidgetItem(str(user.id)))
                self.user_table.setItem(row_idx, 1, QTableWidgetItem(user.username))
                self.user_table.setItem(row_idx, 2, QTableWidgetItem(user.nombre_completo))
                self.user_table.setItem(row_idx, 3, QTableWidgetItem(user.rol))
                self.user_table.setItem(row_idx, 4, QTableWidgetItem(user.estado))
                self.user_table.setItem(row_idx, 5, QTableWidgetItem(user.antiguedad))
                self.user_table.setItem(row_idx, 6, QTableWidgetItem(user.ultimo_editor))

                # Imagen en la columna Foto
                photo_label = QLabel()
                photo_pixmap = QPixmap("source/icons/photo_icon.png").scaled(30, 30, Qt.KeepAspectRatio)
                photo_label.setPixmap(photo_pixmap)
                photo_label.setAlignment(Qt.AlignCenter)
                self.user_table.setCellWidget(row_idx, 7, photo_label)

                # Alinear texto al centro
                for col in range(7):
                    self.user_table.item(row_idx, col).setTextAlignment(Qt.AlignCenter)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los usuarios: {e}")
    
    def add_user(self,user_data=None):
        dialog = UserFormDialog(self, user_data)
        if dialog.exec_():
            self.load_users()  # Recargar tabla después de guardar
        """
        dialog = UserFormDialog(self,user_data)
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
"""
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
