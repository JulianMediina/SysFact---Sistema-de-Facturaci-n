from sqlalchemy import Column, Integer, Date, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Factura(Base):
    __tablename__ = 'factura'
    
    idFactura = Column(Integer, primary_key=True)
    fecha = Column(Date)
    tipo_pago = Column(String(45))
    total = Column(DECIMAL)
    persona_documento = Column(Integer, ForeignKey('persona.documento'))
    
    persona = relationship("Persona")

class DetalleFactura(Base):
    __tablename__ = 'detalle_factura'
    
    idFactura = Column(Integer, ForeignKey('factura.idFactura'), primary_key=True)
    idProducto = Column(Integer, ForeignKey('producto.idProducto'))
    idLote = Column(Integer, ForeignKey('lote.idLote'))
    cantidad = Column(Integer)
    precio = Column(DECIMAL)
    
    factura = relationship("Factura")
    producto = relationship("Producto")
    lote = relationship("Lote")
