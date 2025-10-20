from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import Hospital
from fastapi.staticfiles import StaticFiles
from .models import Hospital

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Transparencia en Salud")

# Servir archivos estáticos (CSS, imágenes, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Directorio de plantillas
templates = Jinja2Templates(directory="app/templates")

# Dependencia para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Página principal
@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Panel de control
@app.get("/panel", response_class=HTMLResponse)
def panel(request: Request, db: Session = Depends(get_db)):
    hospitales = db.query(Hospital).all()

    # Calcular totales
    total_asignado = sum(h.recursos_asignados for h in hospitales)
    total_usado = sum(h.recursos_usados for h in hospitales)
    porcentaje = round((total_usado / total_asignado) * 100, 2) if total_asignado > 0 else 0

    return templates.TemplateResponse(
        "panel.html",
        {
            "request": request,
            "hospitales": hospitales,
            "total_asignado": total_asignado,
            "total_usado": total_usado,
            "porcentaje": porcentaje
        }
    )
@app.get("/productos")
async def obtener_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    return productos
