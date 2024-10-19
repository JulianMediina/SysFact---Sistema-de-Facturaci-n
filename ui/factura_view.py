from PyQt5 import QtWidgets
from models.factura import Factura, DetalleFactura
from models.producto import Producto
from database import session

class FacturaView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Generar Factura')
        
        # Layout
        layout = QtWidgets.QVBoxLayout()

        # Tabla para los detalles de productos
        self.table = QtWidgets.QTableWidget(0, 4)  # Cantidad, Producto, Precio, Total
        self.table.setHorizontalHeaderLabels(['Cantidad', 'Producto', 'Precio', 'Total'])
        layout.addWidget(self.table)

        # Botón para agregar factura
        self.button = QtWidgets.QPushButton('Generar Factura')
        self.button.clicked.connect(self.generar_factura)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def generar_factura(self):
        factura = Factura(total=0)
        session.add(factura)
        session.commit()

        # Logica para crear detalle de factura...
        # Actualizar interfaz o mostrar mensaje
        QtWidgets.QMessageBox.information(self, 'Éxito', 'Factura generada con éxito')
