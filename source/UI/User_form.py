from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QDateEdit, QHBoxLayout, QSpinBox, QFileDialog, QFrame
)
from PyQt5.QtCore import QDate,Qt
from PyQt5.QtGui import QPixmap
from datetime import datetime
import os,shutil
from ..database.crud import agregar_usuario, editar_usuario

class UserFormDialog(QDialog):
    def __init__(self, user_data=None, parent=None):
        super().__init__(parent)
        #quitar icono ? de la ventana
        self.setWindowFlags(
        Qt.Window |
        Qt.CustomizeWindowHint |
        Qt.WindowTitleHint |
        Qt.WindowCloseButtonHint 
        )
        self.setWindowTitle("Agregar Usuario" if not user_data else "Editar Usuario")
        self.setGeometry(400, 200, 500, 600)  # Ajustar tamaño de ventana

        self.user_data = user_data
        self.foto_path = ""  # Para guardar la ruta de la foto
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Campos básicos
        self.nombre_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Ocultar texto
        self.rol_input = QComboBox()
        self.rol_input.addItems(["Administrador", "Cajero"])

        layout.addWidget(QLabel("Nombre Completo:"))
        layout.addWidget(self.nombre_input)

        layout.addWidget(QLabel("Nombre de Usuario:"))
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.password_input)

        layout.addWidget(QLabel("Rol:"))
        layout.addWidget(self.rol_input)

        # Fecha de nacimiento
        self.fecha_nacimiento_input = QDateEdit()
        self.fecha_nacimiento_input.setCalendarPopup(True)
        self.fecha_nacimiento_input.setDate(QDate.currentDate())
        self.fecha_nacimiento_input.dateChanged.connect(self.calcular_edad)

        layout.addWidget(QLabel("Fecha de Nacimiento:"))
        layout.addWidget(self.fecha_nacimiento_input)

        # Edad
        edad_layout = QHBoxLayout()
        self.edad_input = QSpinBox()
        self.edad_input.setRange(0, 120)
        edad_layout.addWidget(QLabel("Edad:"))
        edad_layout.addWidget(self.edad_input)
        layout.addLayout(edad_layout)

        # CURP
        self.curp_input = QLineEdit()
        layout.addWidget(QLabel("CURP:"))
        layout.addWidget(self.curp_input)

        # Fecha de inicio
        self.fecha_inicio_input = QDateEdit()
        self.fecha_inicio_input.setCalendarPopup(True)
        self.fecha_inicio_input.setDate(QDate.currentDate())
        self.fecha_inicio_input.dateChanged.connect(self.calcular_antiguedad)

        layout.addWidget(QLabel("Fecha de Inicio:"))
        layout.addWidget(self.fecha_inicio_input)

        # Antigüedad
        antiguedad_layout = QHBoxLayout()
        self.antiguedad_input = QSpinBox()
        self.antiguedad_input.setRange(0, 50)
        antiguedad_layout.addWidget(QLabel("Antigüedad (años):"))
        antiguedad_layout.addWidget(self.antiguedad_input)
        layout.addLayout(antiguedad_layout)

        # Sección de Foto
        layout.addWidget(QLabel("Foto del Usuario:"))
        foto_layout = QHBoxLayout()

        # Vista previa de la foto
        self.foto_label = QLabel()
        self.foto_label.setFixedSize(120, 120)
        self.foto_label.setFrameStyle(QFrame.Box)
        self.foto_label.setScaledContents(True)
        foto_layout.addWidget(self.foto_label)

        # Botón para seleccionar foto
        self.foto_button = QPushButton("Seleccionar Foto")
        self.foto_button.clicked.connect(self.seleccionar_foto)
        foto_layout.addWidget(self.foto_button)

        layout.addLayout(foto_layout)

        # Botón de guardar
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_user)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Si se edita un usuario, cargar datos previos
        if self.user_data:
            self.load_user_data()

    def load_user_data(self):
        """Cargar datos del usuario en los campos del formulario."""
        self.nombre_input.setText(self.user_data.get("nombre_completo", ""))
        self.username_input.setText(self.user_data.get("username", ""))
        self.password_input.setText("")
        self.rol_input.setCurrentText(self.user_data.get("rol", "Usuario"))

        fecha_nacimiento = self.user_data.get("fecha_nacimiento")
        if fecha_nacimiento:
            self.fecha_nacimiento_input.setDate(QDate.fromString(fecha_nacimiento, "yyyy-MM-dd"))
        self.edad_input.setValue(self.user_data.get("edad", 0))

        self.curp_input.setText(self.user_data.get("curp", ""))

        fecha_inicio = self.user_data.get("fecha_inicio")
        if fecha_inicio:
            self.fecha_inicio_input.setDate(QDate.fromString(fecha_inicio, "yyyy-MM-dd"))
        self.antiguedad_input.setValue(self.user_data.get("antiguedad", 0))

        self.foto_path = self.user_data.get("foto_path", "")
        if self.foto_path:
            self.foto_label.setPixmap(QPixmap(self.foto_path))

    def seleccionar_foto(self):
        """Abrir un diálogo para seleccionar una imagen."""
        foto_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Foto", "", "Imágenes (*.png *.jpg *.jpeg)")
        if foto_path:
            self.foto_path = foto_path
            self.foto_label.setPixmap(QPixmap(self.foto_path))

    def calcular_edad(self):
        fecha_nacimiento = self.fecha_nacimiento_input.date().toPyDate()
        hoy = datetime.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        self.edad_input.setValue(edad)

    def calcular_antiguedad(self):
        fecha_inicio = self.fecha_inicio_input.date().toPyDate()
        hoy = datetime.today()
        antiguedad = hoy.year - fecha_inicio.year - ((hoy.month, hoy.day) < (fecha_inicio.month, fecha_inicio.day))
        self.antiguedad_input.setValue(antiguedad)

    def save_user(self):
        """Guardar usuario."""
        nombre_completo = self.nombre_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        rol = self.rol_input.currentText()
        fecha_nacimiento = self.fecha_nacimiento_input.date().toString("yyyy-MM-dd")
        fecha_inicio = self.fecha_inicio_input.date().toString("yyyy-MM-dd")
        antiguedad = self.antiguedad_input.value()  # Se calculará automáticamente
        curp = self.curp_input.text()
        ultimo_editor = "admin"  # Este campo debe venir del usuario actual en sesión
        """
        # Validar CURP
        if not re.fullmatch(r'^[A-Z0-9]{18}$', curp):
            QMessageBox.warning(self, "Error", "La CURP debe tener 18 caracteres y solo contener letras mayúsculas y números.")
            return
        """
        if not nombre_completo or not username or not password or not curp:
            QMessageBox.warning(self, "Error", "Todos los campos obligatorios deben ser llenados.")
            return

        # Guardar la foto
        foto_path = None
        if self.foto_path:
            try:
                foto_path = self.save_photo(username)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar la foto: {str(e)}")
                return

        # Llamada a la función agregar_usuario
        try:
            agregar_usuario(
                Nombre_completo=nombre_completo,  # Usar el nombre correcto
                username=username, 
                password=password, 
                rol=rol, 
                foto=foto_path, 
                fecha_nacimiento=fecha_nacimiento, 
                fecha_inicio=fecha_inicio, 
                ultimo_editor=ultimo_editor
            )
            QMessageBox.information(self, "Éxito", "Usuario agregado correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar el usuario: {str(e)}")
            raise e

    def save_photo(self, username):
        """Guardar la foto seleccionada y devolver la ruta."""
        # Permitir que el usuario seleccione una foto
        foto_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar foto", "", "Images (*.png *.jpg *.jpeg)")
        if not foto_path:
            return None  # No se seleccionó ninguna foto

        # Crear el directorio donde se guardarán las fotos si no existe
        upload_dir = "uploads/fotos_usuarios"
        os.makedirs(upload_dir, exist_ok=True)

        # Obtener la extensión del archivo seleccionado
        ext = os.path.splitext(foto_path)[1]
        destino = os.path.join(upload_dir, f"{username}{ext}")

        # Copiar la foto al directorio de destino
        try:
            shutil.copy(foto_path, destino)
            return destino  # Devolver la ruta donde se guardó la foto
        except Exception as e:
            raise Exception(f"Error al guardar la foto: {str(e)}")