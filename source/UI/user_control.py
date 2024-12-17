from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt5.QtCore import QDate,Qt
from PyQt5.QtGui import QIcon
from source.database.database import SessionLocal
from .User_form import UserFormDialog
from ..database.crud import agregar_usuario,eliminar_usuario,editar_usuario,listar_usuarios,registrar_actividad
class UserControlWindow(QWidget):
    def __init__(self,logged_user):
        super().__init__()
        self.usuario_logueado=logged_user
        self.setup_ui()
        self.load_styles()
        self.load_users()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Etiqueta de encabezado
        header_label = QLabel("Administración de Usuarios")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header_label)

        # Tabla de usuarios
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["ID", "Nombre", "Usuario", "Rol"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.user_table)

        # Botones de acción
        button_layout = QHBoxLayout()

        add_button = QPushButton("Agregar Usuario")
        add_button.setIcon(QIcon("icons/add-user.png"))
        add_button.clicked.connect(self.add_user)
        button_layout.addWidget(add_button)

        edit_button = QPushButton("Editar Usuario")
        edit_button.setIcon(QIcon("icons/edit-user.png"))
        edit_button.clicked.connect(self.edit_user)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Eliminar Usuario")
        delete_button.setIcon(QIcon("icons/delete-user.png"))
        delete_button.clicked.connect(self.delete_user)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.load_users()
    
    def load_styles(self):
        """Cargar hoja de estilos externa."""
        try:
            with open('source/styles/main.css', 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Archivo de estilo no encontrado: main.css")

    def load_users(self):
        """Cargar datos de usuarios desde la base de datos."""
        self.user_table.setRowCount(0)
        usuarios = listar_usuarios()
        for row, user in enumerate(usuarios):
            self.user_table.insertRow(row)
            self.user_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.user_table.setItem(row, 1, QTableWidgetItem(user.nombre_completo))
            self.user_table.setItem(row, 2, QTableWidgetItem(user.username))
            self.user_table.setItem(row, 3, QTableWidgetItem(user.rol))

    def cargar_datos_formulario(self,row):
        self.ui.inputID.setText(self.ui.tablaUsuarios.item(row, 0).text())
        self.ui.inputNombre.setText(self.ui.tablaUsuarios.item(row, 1).text())
        self.ui.inputUsername.setText(self.ui.tablaUsuarios.item(row, 2).text())
        self.ui.inputRol.setText(self.ui.tablaUsuarios.item(row, 3).text())
        self.ui.inputCURP.setText(self.ui.tablaUsuarios.item(row, 4).text())
        fecha_nac = QDate.fromString(self.ui.tablaUsuarios.item(row, 5).text(), "yyyy-MM-dd")
        self.ui.inputFechaNacimiento.setDate(fecha_nac)
        self.ui.inputFechaInicio.setText(self.ui.tablaUsuarios.item(row, 7).text())

    def add_user(self):
        dialog = UserFormDialog(self.usuario_logueado)
        if dialog.exec_():
            QMessageBox.information(self, "Éxito", "Usuario agregado correctamente.")
            self.load_users()
    
    def edit_user(self):
        """Función para editar usuario."""
        selected_row = self.user_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona una casilla del renglon de usuario para editar.")
            return

        # Obtener el ID del usuario seleccionado
        user_id = int(self.user_table.item(selected_row, 0).text())

        # Obtener los datos actuales del usuario
        user_data = {
            "id": user_id,
            "nombre_completo": self.user_table.item(selected_row, 1).text(),
            "username": self.user_table.item(selected_row, 2).text(),
            "rol": self.user_table.item(selected_row, 3).text()
        }

        # Crear y mostrar el diálogo de edición
        dialog = UserFormDialog(self.usuario_logueado, user_data)  # Pasamos los datos actuales al formulario
        if dialog.exec_():  # Si el usuario presiona "Guardar"
            # Actualizar los datos en la base de datos
            try:
                editar_usuario(dialog.user_data)  # `dialog.user_data` debe contener los datos actualizados
                QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente.")
                self.load_users()  # Recargar la tabla con los datos actualizados
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo actualizar el usuario.\n{str(e)}")

    def delete_user(self):
        """Función para eliminar usuario."""
        selected_row = self.user_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona un usuario para eliminar.")
            return

        # Obtener el ID del usuario seleccionado
        user_id = int(self.user_table.item(selected_row, 0).text())

        # Confirmar la eliminación
        confirm = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            "¿Estás seguro de que deseas eliminar este usuario?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                eliminar_usuario(user_id)  # Llamar a la función del CRUD
                QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente.")
                self.load_users()  # Recargar la tabla
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el usuario.\n{str(e)}")
