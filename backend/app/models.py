from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Hospital(Base):
    __tablename__ = "hospitales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    recursos_asignados = Column(Float, nullable=False)
    recursos_usados = Column(Float, nullable=False)