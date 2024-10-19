from PyQt5 import QtWidgets
from ui.factura_view import FacturaView

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema de Facturación Veterinaria')
        self.setGeometry(100, 100, 800, 600)

        # Crear vistas
        self.factura_view = FacturaView()

        # Crear un menú
        menubar = self.menuBar()
        facturacion_menu = menubar.addMenu('Facturación')
        generar_factura = QtWidgets.QAction('Generar Factura', self)
        generar_factura.triggered.connect(self.mostrar_factura_view)
        facturacion_menu.addAction(generar_factura)

    def mostrar_factura_view(self):
        self.setCentralWidget(self.factura_view)
