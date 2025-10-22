# Importaciones adicionales
from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import Hospital, Usuario
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import timedelta
from sqlalchemy import Boolean
from . import auth
from typing import Optional

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

# Ruta de login
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.post("/login")
async def login(
    request: Request,
    db: Session = Depends(get_db),
    email: str = Form(...),
    password: str = Form(...)
):
    user = auth.authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Correo o contraseña incorrectos"}
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    response = RedirectResponse(url="/panel", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,  # 30 minutos
        expires=1800,
    )
    return response

# Ruta de registro
@app.get("/registro", response_class=HTMLResponse)
def registro_page(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse("registro.html", {"request": request, "error": error})

@app.post("/registro")
async def registro(
    request: Request,
    db: Session = Depends(get_db),
    nombre: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    terms: Optional[str] = Form(None)
):
    # Verificar si las contraseñas coinciden
    if password != confirm_password:
        return templates.TemplateResponse(
            "registro.html", 
            {"request": request, "error": "Las contraseñas no coinciden"}
        )
    
    # Verificar si el usuario ya existe
    existing_user = db.query(Usuario).filter(Usuario.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            "registro.html", 
            {"request": request, "error": "Este correo ya está registrado"}
        )
    
    # Crear nuevo usuario
    hashed_password = auth.get_password_hash(password)
    nuevo_usuario = Usuario(
        email=email,
        nombre=nombre,
        hashed_password=hashed_password,
        es_activo=True,
        es_admin=False
    )
    db.add(nuevo_usuario)
    db.commit()
    
    # Redirigir a login
    return RedirectResponse(url="/login?registro=exitoso", status_code=status.HTTP_303_SEE_OTHER)

# Ruta de logout
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

# Función para obtener el usuario actual desde la cookie
async def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    try:
        token = token.replace("Bearer ", "")
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        user = db.query(Usuario).filter(Usuario.email == email).first()
        return user
    except:
        return None
    
# Panel de control (protegido)
@app.get("/panel", response_class=HTMLResponse)
async def panel(
    request: Request, 
    db: Session = Depends(get_db)
):
    # Verificar autenticación
    user = await get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
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
            "porcentaje": porcentaje,
            "usuario": user
        }
    )

# Agregar hospital
@app.post("/agregar_hospital")
async def agregar_hospital(
    hospital: HospitalCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_active_user)
):
    nuevo_hospital = Hospital(**hospital.dict())
    db.add(nuevo_hospital)
    db.commit()
    db.refresh(nuevo_hospital)
    return JSONResponse(content={"success": True, "id": nuevo_hospital.id})

# Actualizar hospital
@app.put("/actualizar_hospital/{hospital_id}")
async def actualizar_hospital(
    hospital_id: int, 
    hospital: HospitalCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_active_user)
):
    db_hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not db_hospital:
        raise HTTPException(status_code=404, detail="Hospital no encontrado")
    for key, value in hospital.dict().items():
        setattr(db_hospital, key, value)
    db.commit()
    return JSONResponse(content={"success": True})

# Eliminar hospital
@app.delete("/eliminar_hospital/{hospital_id}")
async def eliminar_hospital(
    hospital_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_active_user)
):
    db_hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not db_hospital:
        raise HTTPException(status_code=404, detail="Hospital no encontrado")
    db.delete(db_hospital)
    db.commit()
    return JSONResponse(content={"success": True})
