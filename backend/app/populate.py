from .database import Base, engine
from .models import Hospital

# Crear tablas
Base.metadata.create_all(bind=engine)

# Insertar datos iniciales
from sqlalchemy.orm import Session

session = Session(bind=engine)

hospitales = [
    Hospital(nombre="Hospital San José", ciudad="Bogotá", recursos_asignados=120000000, recursos_usados=85000000),
    Hospital(nombre="Clínica del Norte", ciudad="Medellín", recursos_asignados=95000000, recursos_usados=72000000),
    Hospital(nombre="Hospital Central de Cali", ciudad="Cali", recursos_asignados=105000000, recursos_usados=95000000),
    Hospital(nombre="Hospital Regional de Suba", ciudad="Bogotá", recursos_asignados=80000000, recursos_usados=40000000),
]

session.add_all(hospitales)
session.commit()
session.close()

print("Tabla 'hospitales' creada e inicializada con datos.")
