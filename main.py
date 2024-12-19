import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from source.UI.login_ui import LoginWindow
from source.UI.main_window import MainWindow
from source.database.database import init_db

class App:
    def __init__(self):
        self.app = QApplication([])
        self.app.setWindowIcon(QIcon('source/icons/logo.jpeg'))
        try:
            # Intentamos conectar a la base de datos
            init_db()
        except Exception as e:
            # Si hay un error, mostramos un mensaje y cerramos la app
            QMessageBox.critical(None, "Error de conexión", f"No se pudo conectar a la base de datos:\n{e}")
            sys.exit(1)  # Cierra la aplicación con un código de error

        # Configuración de la ventana de login
        self.login = LoginWindow()
        self.login.setWindowFlags(Qt.Window |
        Qt.CustomizeWindowHint |
        Qt.WindowTitleHint |
        Qt.WindowCloseButtonHint)  # Eliminar ícono
        """
            Qt.Window: Mantiene la funcionalidad de ventana normal.
            Qt.WindowTitleHint: Permite mostrar el título de la ventana.
            Qt.CustomizeWindowHint: Elimina características adicionales, como el ícono.
        """

    def run(self):
        self.login.exec_()
        self.app.exec_()

if __name__ == "__main__":
    try:
        app = App()
        app.run()
    except FileNotFoundError:
        print("Archivo de estilo no encontrado: login.css")
