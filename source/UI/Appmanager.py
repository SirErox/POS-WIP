# app_manager.py
from PyQt5.QtWidgets import QApplication
from source.UI.login_ui import LoginWindow
from source.UI.main_window import MainWindow

class AppManager:
    def __init__(self):
        self.app=QApplication([])
        self.login_window = None
        self.main_window = None
        self.cargar_estilos()

    def cargar_estilos(self):
        """Carga la hoja de estilos de la aplicación."""
        try:
            with open('source/styles/styles.css', 'r') as f:
                self.app.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Archivo de estilo no encontrado: styles.css")
        except Exception as e:
            print(f"Error al cargar la hoja de estilos: {e}")
            
    def iniciar(self):
        """Inicia la aplicación mostrando la ventana de login."""
        self.mostrar_login()
        self.app.exec_()
    #ventana login
    def mostrar_login(self):
        """Abre la ventana de login."""
        if self.main_window:
            self.main_window.close()  # Cierra la ventana principal si está abierta
            self.main_window = None
        self.login_window = LoginWindow(self)
        self.login_window.show()
    #ventana main_window
    def mostrar_main_window(self, usuario):
        """Abre la ventana principal."""
        if self.login_window:
            self.login_window.close()  # Cierra la ventana de login si está abierta
            self.login_window = None
        self.main_window = MainWindow(self, usuario)
        self.main_window.show()
