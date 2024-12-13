from PyQt5.QtWidgets import(QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QMessageBox)

class MainWindow(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("POS System - Ventana Principal")
        self.setFixedSize(800, 600)
        layout = QVBoxLayout()
        
        # Botón para Ventas (Disponible para ambos roles)
        ventas_button = QPushButton("Realizar Venta")
        ventas_button.clicked.connect(self.abrir_ventana_ventas)
        layout.addWidget(ventas_button)

        # Botón para Gestión (Solo para Administradores)
        if usuario.rol == 'administrador':
            gestion_button = QPushButton("Gestión de Inventario")
            gestion_button.clicked.connect(self.abrir_gestion_inventario)
            layout.addWidget(gestion_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def abrir_ventana_ventas(self):
        QMessageBox.information(self, "Ventas", "Abriendo la ventana de ventas...")

    def abrir_gestion_inventario(self):
        QMessageBox.information(self, "Gestión de Inventario", "Abriendo la gestión de inventario...")

