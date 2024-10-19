from PyQt5 import QtWidgets
from models.usuario import Usuario, es_vendedor, es_cliente
from database import session

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inicio de Sesión')
        self.setGeometry(100, 100, 280, 80)
        
        # Layout
        layout = QtWidgets.QVBoxLayout()

        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Usuario")
        layout.addWidget(self.username)

        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password)

        self.button = QtWidgets.QPushButton('Iniciar Sesión', self)
        self.button.clicked.connect(self.iniciar_sesion)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def iniciar_sesion(self):
        login = self.username.text()
        clave = self.password.text()
        
        usuario = session.query(Usuario).filter_by(login=login, clave=clave).first()
        
        if usuario:
            if es_vendedor(usuario):
                print("Acceso permitido a funciones de vendedor")
                # Abrir la ventana principal del vendedor
            elif es_cliente(usuario):
                print("Acceso permitido a funciones de cliente")
                # Abrir una ventana limitada para el cliente
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Usuario o contraseña incorrectos')
