from fastapi import FastAPI
from .database import Base, engine
from .routers import productos, usuarios  # Aún puedes crear estos routers después

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend Web Salud")

# Incluir routers (si no los tienes aún, puedes comentar estas líneas temporalmente)
# app.include_router(productos.router)
# app.include_router(usuarios.router)

@app.get("/")
def root():
    return {"mensaje": "API Web Salud funcionando"}
