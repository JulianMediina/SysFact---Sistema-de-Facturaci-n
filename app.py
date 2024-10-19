from PyQt5 import QtWidgets
from ui.login_window import LoginWindow
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
