from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QDateEdit,
    QHBoxLayout, QSpinBox, QFileDialog, QFrame, QGridLayout)
from PyQt5.QtCore import QDate,Qt
from PyQt5.QtGui import QPixmap,QIcon
from datetime import datetime
import os,shutil,re
from ..database.crud import agregar_usuario, editar_usuario

class UserFormDialog(QDialog):
    def __init__(self, logged_user,user_data=None, parent=None):
        super().__init__(parent)
        self.usuario_logueado=logged_user
        self.user_data = user_data
        self.foto_path = ""  # Para guardar la ruta de la foto
        #quitar icono ? de la ventana
        self.setWindowFlags(
        Qt.Window |
        Qt.CustomizeWindowHint |
        Qt.WindowTitleHint |
        Qt.WindowCloseButtonHint 
        )
        self.setWindowTitle("Agregar Usuario" if not user_data else "Editar Usuario")
        self.setWindowIcon(QIcon('source/icons/logo.jpeg'))
        self.resize(500, 400)  # Ajustar tamaño de ventana

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(10)  # Espaciado entre widgets
        layout.setContentsMargins(10, 10, 10, 10)

        # Nombre Completo
        layout.addWidget(QLabel("Nombre Completo:"), 0, 0)
        self.nombre_input = QLineEdit()
        layout.addWidget(self.nombre_input, 0, 1, 1, 2)

        # Nombre de Usuario
        layout.addWidget(QLabel("Nombre de Usuario:"), 1, 0)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input, 1, 1, 1, 2)

        # Contraseña
        layout.addWidget(QLabel("Contraseña:"), 2, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input, 2, 1, 1, 2)

        # Rol
        layout.addWidget(QLabel("Rol:"), 3, 0)
        self.rol_input = QComboBox()
        self.rol_input.addItems(["administrador", "Cajero"])
        layout.addWidget(self.rol_input, 3, 1, 1, 2)

        # Fecha de Nacimiento
        layout.addWidget(QLabel("Fecha de Nacimiento:"), 4, 0)
        self.fecha_nacimiento_input = QDateEdit()
        self.fecha_nacimiento_input.setCalendarPopup(True)
        self.fecha_nacimiento_input.setDate(QDate.currentDate())
        self.fecha_nacimiento_input.dateChanged.connect(self.calcular_edad)
        layout.addWidget(self.fecha_nacimiento_input, 4, 1)

        # Edad
        layout.addWidget(QLabel("Edad:"), 4, 2)
        self.edad_input = QSpinBox()
        self.edad_input.setRange(0, 120)
        layout.addWidget(self.edad_input, 4, 3)

        # CURP
        layout.addWidget(QLabel("CURP:"), 5, 0)
        self.curp_input = QLineEdit()
        self.curp_input.setPlaceholderText("CURP AQUI")
        self.curp_input.textChanged.connect(self.convert_to_mayus)
        layout.addWidget(self.curp_input, 5, 1, 1, 3)

        # Fecha de Inicio
        layout.addWidget(QLabel("Fecha de Inicio:"), 6, 0)
        self.fecha_inicio_input = QDateEdit()
        self.fecha_inicio_input.setCalendarPopup(True)
        self.fecha_inicio_input.setDate(QDate.currentDate())
        self.fecha_inicio_input.dateChanged.connect(self.calcular_antiguedad)
        layout.addWidget(self.fecha_inicio_input, 6, 1)

        # Antigüedad
        layout.addWidget(QLabel("Antigüedad (años):"), 6, 2)
        self.antiguedad_input = QSpinBox()
        self.antiguedad_input.setRange(0, 50)
        layout.addWidget(self.antiguedad_input, 6, 3)

        # Foto del Usuario
        layout.addWidget(QLabel("Foto del Usuario:"), 7, 0)
        self.foto_label = QLabel()
        self.foto_label.setFixedSize(100, 100)
        self.foto_label.setFrameStyle(QFrame.Box)
        self.foto_label.setScaledContents(True)
        layout.addWidget(self.foto_label, 7, 1)

        self.foto_button = QPushButton("Seleccionar Foto")
        self.foto_button.clicked.connect(self.seleccionar_foto)
        layout.addWidget(self.foto_button, 7, 2, 1, 2)

        # Botón de Guardar
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_user)
        layout.addWidget(save_button, 8, 0, 1, 4)

        self.setLayout(layout)

        # Si es edición, cargar datos previos
        if self.user_data:
            self.load_user_data()

    def convert_to_mayus(self):
        # Obtener el texto actual y convertirlo a mayúsculas
        texto_actual = self.curp_input.text()
        self.curp_input.setText(texto_actual.upper())

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
        curp = self.curp_input.text().upper()
        
        if not nombre_completo or not username or not password or not curp:
            QMessageBox.warning(self, "Error", "Todos los campos obligatorios deben ser llenados.")
            return

        # Validar CURP
        if not re.fullmatch(r'^[A-Z0-9]{18}$', curp):
            QMessageBox.warning(self, "Error", "La CURP debe tener 18 caracteres y solo contener letras mayúsculas y números.")
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
            ultimo_editor = self.usuario_logueado  # Asegúrate de tener esta variable en tu clase
            if self.user_data:  # Editar usuario
                editar_usuario(
                    self.user_data.get("id"),
                    nombre_completo=nombre_completo,
                    username=username,
                    password=password,
                    rol=rol,
                    foto=foto_path,
                    fecha_nacimiento=fecha_nacimiento,
                    fecha_inicio=fecha_inicio,
                    curp=curp,
                    ultimo_editor=ultimo_editor
                )
                QMessageBox.information(self, "Éxito", "Usuario editado correctamente.")
            else:  # Agregar usuario
                agregar_usuario(
                    nombre_completo=nombre_completo,
                    username=username,
                    password=password,
                    rol=rol,
                    foto=foto_path,
                    fecha_nacimiento=fecha_nacimiento,
                    fecha_inicio=fecha_inicio,
                    curp=curp,
                    ultimo_editor=ultimo_editor
                )
                QMessageBox.information(self, "Éxito", "Usuario agregado correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")

    def save_photo(self, username):
        """Guardar la foto seleccionada y devolver la ruta."""
        if not self.foto_path:
            return None  # Si no se seleccionó foto, retorna None

        # Crear el directorio donde se guardarán las fotos si no existe
        upload_dir = os.path.join("source", "imagenes", "usuarios")
        os.makedirs(upload_dir, exist_ok=True)

        # Obtener la extensión del archivo seleccionado
        ext = os.path.splitext(self.foto_path)[1]
        destino = os.path.join(upload_dir, f"{username}{ext}")

        # Copiar la foto al directorio de destino
        try:
            # Usa la ruta de la foto original como bytes
            with open(self.foto_path, 'rb') as src_file:
                with open(destino, 'wb') as dest_file:
                    shutil.copyfileobj(src_file, dest_file)  # Copiar contenido
            return destino  # Devolver la ruta donde se guardó la foto
        except Exception as e:
            raise Exception(f"Error al guardar la foto: {str(e)}")