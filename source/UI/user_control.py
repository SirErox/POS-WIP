from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem

class UserControlWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Usuarios")
        self.setGeometry(150, 150, 500, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta
        label = QLabel("Lista de Usuarios")
        layout.addWidget(label)

        # Tabla de usuarios
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Rol"])
        layout.addWidget(self.table)

        # Botón de cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        # Cargar datos de ejemplo (puedes adaptarlo para obtener datos reales)
        self.load_users()

    def load_users(self):
        # Aquí puedes conectar con tu base de datos para cargar los usuarios
        usuarios = [
            {"id": 1, "nombre": "Admin", "rol": "administrador"},
            {"id": 2, "nombre": "Cajero 1", "rol": "cajero"},
        ]

        self.table.setRowCount(len(usuarios))
        for row, usuario in enumerate(usuarios):
            self.table.setItem(row, 0, QTableWidgetItem(str(usuario["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(usuario["nombre"]))
            self.table.setItem(row, 2, QTableWidgetItem(usuario["rol"]))
