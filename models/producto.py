from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Producto(Base):
    __tablename__ = 'producto'
    
    idProducto = Column(Integer, primary_key=True)
    nombre = Column(String(45))
    unidadMedida = Column(String(45))

class Lote(Base):
    __tablename__ = 'lote'
    
    idLote = Column(Integer, primary_key=True)
    fecha_fabricacion = Column(Date)

class ProductoLote(Base):
    __tablename__ = 'productolote'
    
    idProducto = Column(Integer, ForeignKey('producto.idProducto'), primary_key=True)
    idLote = Column(Integer, ForeignKey('lote.idLote'), primary_key=True)
    cantidad = Column(Integer)
    fecha_vencimiento = Column(Date)
    precio = Column(DECIMAL)
    
    producto = relationship("Producto")
    lote = relationship("Lote")
