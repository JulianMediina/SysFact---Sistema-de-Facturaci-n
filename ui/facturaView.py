from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QPushButton, QLabel, QLineEdit, QDateEdit, QDialog
import sys
from datetime import date
from sqlalchemy.orm import sessionmaker
#from database import engine
from models.factura import Factura, DetalleFactura
from models.producto import Producto, Lote, ProductoLote
from models.usuario import Persona, Usuario
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Conexión a la base de datos MySQL
DATABASE_URI = 'mysql+pymysql://root:12345@localhost:3306/facturacion'

# Motor de la base de datos
engine = create_engine(DATABASE_URI)

# Sesión de la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Base para las clases ORM
Base = declarative_base()

# Crear todas las tablas si no existen
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class FacturacionWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Facturación")
        self.layout = QVBoxLayout()
        self.resize(800, 600)  # Cambiar el tamaño de la ventana a 800x600 píxeles

        # Número de factura (consecutivo)
        self.label_numero_factura = QLabel(f"Factura N°: {self.get_numero_factura()}")
        self.layout.addWidget(self.label_numero_factura)

        # Fecha actual
        self.label_fecha = QLabel(f"Fecha: {date.today()}")
        self.layout.addWidget(self.label_fecha)

        # Documento del cliente
        self.label_documento = QLabel("Documento del Cliente:")
        self.input_documento = QLineEdit()
        self.input_documento.returnPressed.connect(self.buscar_cliente)
        self.layout.addWidget(self.label_documento)
        self.layout.addWidget(self.input_documento)

        # Datos del cliente
        self.label_cliente_info = QLabel("Nombre: \nDirección: \nEmail: \nTeléfono:")
        self.layout.addWidget(self.label_cliente_info)

        # Tabla de productos
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Cantidad", "Detalle", "Precio Unitario", "Precio Total"])
        self.layout.addWidget(self.table)

        # Subtotal, IVA y Total
        self.label_subtotal = QLabel("Subtotal: 0.0")
        self.label_iva = QLabel("IVA (19%): 0.0")
        self.label_total = QLabel("Total a Pagar: 0.0")
        self.layout.addWidget(self.label_subtotal)
        self.layout.addWidget(self.label_iva)
        self.layout.addWidget(self.label_total)

        # Selección de medio de pago
        self.label_medio_pago = QLabel("Medio de Pago:")
        self.combo_medio_pago = QComboBox()
        self.combo_medio_pago.addItems(["Efectivo", "Tarjeta"])
        self.layout.addWidget(self.label_medio_pago)
        self.layout.addWidget(self.combo_medio_pago)

        # Selección de vendedor
        self.label_vendedor = QLabel("Vendedor:")
        self.combo_vendedor = QComboBox()
        self.load_vendedores()
        self.layout.addWidget(self.label_vendedor)
        self.layout.addWidget(self.combo_vendedor)

        # Botones
        self.btn_add_producto = QPushButton("Añadir Producto")
        self.btn_add_producto.clicked.connect(self.abrir_ventana_productos)
        self.layout.addWidget(self.btn_add_producto)

        self.btn_guardar_factura = QPushButton("Guardar Factura")
        self.btn_guardar_factura.clicked.connect(self.guardar_factura)
        self.layout.addWidget(self.btn_guardar_factura)

        self.setLayout(self.layout)

    def get_numero_factura(self):
        factura = session.query(Factura).order_by(Factura.idfactura.desc()).first()
        return factura.idfactura + 1 if factura else 1

    def buscar_cliente(self):
        documento = self.input_documento.text()
        cliente = session.query(Persona).filter_by(documento=documento).first()
        if cliente:
            self.label_cliente_info.setText(f"Nombre: {cliente.nombres} {cliente.apellidos}\n"
                                            f"Dirección: {cliente.direccion}\n"
                                            f"Email: {cliente.correo}\n"
                                            f"Teléfono: {cliente.telefono}")
        else:
            self.label_cliente_info.setText("Cliente no encontrado")

    def abrir_ventana_productos(self):
        self.dialog = ProductosWindow(self)
        self.dialog.exec_()

    def actualizar_total(self):
        subtotal = 0.0
        for row in range(self.table.rowCount()):
            subtotal += float(self.table.item(row, 3).text())

        iva = subtotal * 0.19
        total = subtotal + iva

        self.label_subtotal.setText(f"Subtotal: {subtotal:.2f}")
        self.label_iva.setText(f"IVA (19%): {iva:.2f}")
        self.label_total.setText(f"Total a Pagar: {total:.2f}")

    def load_vendedores(self):
        vendedores = session.query(Usuario).filter_by(tipo='vendedor').all()
        for vendedor in vendedores:
            self.combo_vendedor.addItem(f"{vendedor.persona.nombres} {vendedor.persona.apellidos}", vendedor.login)

    def guardar_factura(self):
        documento_cliente = self.input_documento.text()
        cliente = session.query(Persona).filter_by(documento=documento_cliente).first()

        if not cliente:
            QtWidgets.QMessageBox.warning(self, "Error", "Cliente no encontrado")
            return

        vendedor_id = self.combo_vendedor.currentData()
        total = float(self.label_total.text().split(":")[1])

        # Crear la factura
        nueva_factura = Factura(
            fecha=date.today(),
            tipo_pago=self.combo_medio_pago.currentText(),
            total=total,
            persona_documento=cliente.documento
        )
        session.add(nueva_factura)
        session.commit()

        # Añadir los detalles de la factura
        for row in range(self.table.rowCount()):
            id_producto = self.table.item(row, 0).data(QtCore.Qt.UserRole)
            cantidad = int(self.table.item(row, 0).text())
            precio_unitario = float(self.table.item(row, 2).text())
            lote_id = self.table.item(row, 0).data(QtCore.Qt.UserRole + 1)  # ID del lote

            detalle = DetalleFactura(
                cantidad=cantidad,
                iva = 19,
                factura_idfactura =self.get_numero_factura(),
                producto_idProducto = id_producto
            )
            session.add(detalle)
        
        productolote = session.query(ProductoLote).filter_by(idProducto=id_producto, idLote=lote_id).first()

        if productolote is not None:
            productolote.cantidad -= cantidad  # Restar la cantidad de la propiedad cantidad
            session.commit()  # No olvides hacer commit para guardar los cambios en la base de datos
        else:
            print("No se encontró el productolote.")

 

        session.commit()
        QtWidgets.QMessageBox.information(self, "Éxito", "Factura guardada correctamente")


class ProductosWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Seleccionar Producto")
        self.layout = QVBoxLayout()

        # Tabla para mostrar productos disponibles
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Producto", "Nombre", "Unidad", "Precio"])
        self.layout.addWidget(self.table)

        self.btn_add = QPushButton("Agregar Producto")
        self.btn_add.clicked.connect(self.add_producto)
        self.layout.addWidget(self.btn_add)

        self.setLayout(self.layout)
        self.load_productos()

    def load_productos(self):
        productos_lote = session.query(ProductoLote).filter(ProductoLote.cantidad > 0).all()

        self.table.setRowCount(len(productos_lote))
        for row, producto_lote in enumerate(productos_lote):
            producto = producto_lote.producto
            lote = producto_lote.lote

            self.table.setItem(row, 0, QTableWidgetItem(str(producto.idProducto)))
            self.table.setItem(row, 1, QTableWidgetItem(producto.nombre))
            self.table.setItem(row, 2, QTableWidgetItem(producto.unidadMedida))
            self.table.setItem(row, 3, QTableWidgetItem(str(producto_lote.precio)))

    def add_producto(self):
        row = self.table.currentRow()

        id_producto = int(self.table.item(row, 0).text())
        nombre = self.table.item(row, 1).text()
        unidad = self.table.item(row, 2).text()
        precio_unitario = float(self.table.item(row, 3).text())

        parent_table = self.parent().table
        parent_row = parent_table.rowCount()
        parent_table.insertRow(parent_row)

        cantidad_item = QTableWidgetItem("1")
        cantidad_item.setData(QtCore.Qt.UserRole, id_producto)
        parent_table.setItem(parent_row, 0, cantidad_item)

        detalle_item = QTableWidgetItem(f"{unidad} {nombre}")
        parent_table.setItem(parent_row, 1, detalle_item)

        precio_unitario_item = QTableWidgetItem(f"{precio_unitario:.2f}")
        parent_table.setItem(parent_row, 2, precio_unitario_item)

        precio_total_item = QTableWidgetItem(f"{precio_unitario:.2f}")
        parent_table.setItem(parent_row, 3, precio_total_item)

        # Actualizar los totales en la factura
        self.parent().actualizar_total()
        self.close()


