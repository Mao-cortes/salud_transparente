from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base
from sqlalchemy.sql.schema import ForeignKey

class Hospital(Base):
    __tablename__ = "hospitales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    recursos_asignados = Column(Float, nullable=False)
    recursos_usados = Column(Float, nullable=False)

# Añadir a models.py
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    es_activo = Column(Boolean, default=True)
    es_admin = Column(Boolean, default=False)
