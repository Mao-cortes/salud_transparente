from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import Hospital
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
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

# Modelo Pydantic para la validación de datos
class HospitalCreate(BaseModel):
    nombre: str
    ciudad: str
    recursos_asignados: float
    recursos_usados: float

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

# Agregar hospital
@app.post("/agregar_hospital")
def agregar_hospital(hospital: HospitalCreate, db: Session = Depends(get_db)):
    nuevo_hospital = Hospital(**hospital.dict())
    db.add(nuevo_hospital)
    db.commit()
    db.refresh(nuevo_hospital)
    return JSONResponse(content={"success": True, "id": nuevo_hospital.id})

# Actualizar hospital
@app.put("/actualizar_hospital/{hospital_id}")
def actualizar_hospital(hospital_id: int, hospital: HospitalCreate, db: Session = Depends(get_db)):
    db_hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not db_hospital:
        raise HTTPException(status_code=404, detail="Hospital no encontrado")
    for key, value in hospital.dict().items():
        setattr(db_hospital, key, value)
    db.commit()
    return JSONResponse(content={"success": True})

# Eliminar hospital
@app.delete("/eliminar_hospital/{hospital_id}")
def eliminar_hospital(hospital_id: int, db: Session = Depends(get_db)):
    db_hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not db_hospital:
        raise HTTPException(status_code=404, detail="Hospital no encontrado")
    db.delete(db_hospital)
    db.commit()
    return JSONResponse(content={"success": True})

