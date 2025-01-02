# app_manager.py
from PyQt5.QtWidgets import QApplication
from source.UI.login_ui import LoginWindow
from source.UI.main_window import MainWindow
from source.database.crud import CRUDUsuarios,CRUDInventario #importamos la clase CRU
from source.database.database import SessionLocal

class AppManager:
    def __init__(self):
        self.app=QApplication([])
        self.login_window = None
        self.main_window = None
        self.db_session = SessionLocal()
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

    def cerrar_sesion(self):
        """Cierra la sesión del usuario y vuelve al login."""
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        self.mostrar_login()

    def cerrar_aplicacion(self):
        """Cierra la aplicación y limpia recursos."""
        if self.db_session:
            self.db_session.close()  # Cierra la sesión de la base de datos
        self.app.quit()

    def registrar_venta(self, datos_venta):
        """
        Registra una venta utilizando el CRUD y maneja transacciones.
        Args:
            datos_venta (dict): Diccionario con la información de la venta (productos, cliente, total, etc.).
        Returns:
            int: ID de la venta registrada.
        """
        try:
            # Validaciones previas
            if not datos_venta.get("productos"):
                raise ValueError("La venta debe incluir al menos un producto.")

            # Llamada al CRUD para registrar la venta
            venta_id = self.crud.registrar_venta(self.db_session, **datos_venta)

            # Confirmar la transacción
            self.db_session.commit()

            return venta_id
        except Exception as e:
            self.db_session.rollback()  # Revertir cambios si ocurre un error
            print(f"Error al registrar la venta: {e}")
            raise e

