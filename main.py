import sys
from PyQt5.QtWidgets import QApplication
from source.UI.login_ui import LoginWindow
from database import init_db
def main():
    init_db()
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()