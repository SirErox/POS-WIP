import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from source.UI.login_ui import LoginWindow
from source.UI.main_window import MainWindow
from source.database.database import init_db
from source.UI.Appmanager import AppManager

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QIcon('source/icons/logo.jpeg'))

        # Cargar y aplicar la hoja de estilos
        try:
            with open('source/styles/styles.css', 'r') as f:
                self.app.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Archivo de estilo no encontrado: styles.css")
        except Exception as e:
            print(f"Error al cargar la hoja de estilos: {e}")

        try:
            # Intentamos conectar a la base de datos
            init_db()
        except Exception as e:
            QMessageBox.critical(None, "Error de conexión", f"No se pudo conectar a la base de datos:\n{e}")
            sys.exit(1)  # Cierra la aplicación con un código de error

        # Configuración de la ventana de login
        self.login = LoginWindow()
        self.login.setWindowFlags(Qt.Window |
                                   Qt.CustomizeWindowHint |
                                   Qt.WindowTitleHint |
                                   Qt.WindowCloseButtonHint)

        # Variable para asegurar que solo una instancia de MainWindow exista
        self.main_window = None

    def run(self):
        if self.login.exec_() == QDialog.Accepted:
            # Asegúrate de no crear múltiples ventanas
            if not self.main_window:
                self.main_window = MainWindow(self.login.usuario)
                self.main_window.show()
            sys.exit(self.app.exec_())  # Ejecuta el bucle de eventos

if __name__ == "__main__":
    app_manager = AppManager()
    app_manager.iniciar()
