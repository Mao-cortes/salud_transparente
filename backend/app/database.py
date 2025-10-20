from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# URL de la base de datos SQLite (archivo database.db en la carpeta backend)
DATABASE_URL = "sqlite:///./database.db"
# Crear motor de conexión
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base para los modelos
Base = declarative_base()
# Dependencia para obtener sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
