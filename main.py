import sys
from PyQt5.QtWidgets import QApplication, QDialog
from source.UI.login_ui import LoginWindow
from source.UI.main_window import MainWindow
from database import init_db
def main():
    #iniciamos la conexion con la base de datos
    init_db()
    app = QApplication(sys.argv)
    #mostramos la ventana de login
    login=LoginWindow()
    if login.exec_() == QDialog.Accepted:
        usuario = login.usuario
        mainWindow=MainWindow(usuario)
        mainWindow.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()