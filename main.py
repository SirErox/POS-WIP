import sys
from PyQt5.QtWidgets import QApplication
from source.login_ui import LoginWindow
from source.crud import agregar_usuario,listar_usuarios

#resultado=agregar_usuario("David","admin","admin123","administrador")
#print(resultado)

usuarios=listar_usuarios()
for usuario in usuarios:
    print(f"ID: {usuario.id}, Nombre: {usuario.nombre}, Username: {usuario.username}, Rol: {usuario.rol}")

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()