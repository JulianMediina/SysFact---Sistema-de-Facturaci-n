from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Persona(Base):
    __tablename__ = 'persona'
    
    documento = Column(Integer, primary_key=True)
    tipo_documento = Column(String(20))
    nombres = Column(String(45))
    apellidos = Column(String(45))
    correo = Column(String(45))
    direccion = Column(String(45))
    telefono = Column(String(20))

class Usuario(Base):
    __tablename__ = 'usuario'
    
    login = Column(Integer, primary_key=True)
    clave = Column(String(20))
    tipo = Column(String(10))  # 'vendedor' o 'cliente'
    persona_documento = Column(Integer, ForeignKey('persona.documento'))
    
    persona = relationship("Persona")

# Funciones para diferenciar entre vendedores y clientes
def es_vendedor(usuario):
    return usuario.tipo == 'vendedor'

def es_cliente(usuario):
    return usuario.tipo == 'cliente'
