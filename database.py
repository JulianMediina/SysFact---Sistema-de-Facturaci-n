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
