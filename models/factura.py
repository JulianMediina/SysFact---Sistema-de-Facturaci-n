from sqlalchemy import Column, Integer, Date, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Factura(Base):
    __tablename__ = 'factura'
    idfactura = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=True)
    tipo_pago = Column(String(45), nullable=True)
    total = Column(DECIMAL(10,2), nullable=True)
    persona_documento = Column(Integer, ForeignKey('persona.documento'))
    
    persona = relationship("Persona")

class DetalleFactura(Base):
    __tablename__ = 'detallefactura'
    
    cantidad = Column(Integer)
    iva = Column(Integer)        
    factura_idfactura = Column(Integer, ForeignKey('factura.idfactura'), primary_key=True)
    producto_idProducto = Column(Integer, ForeignKey('producto.idProducto'))
    
    factura = relationship("Factura")
    producto = relationship("Producto")
    
