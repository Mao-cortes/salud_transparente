from pydantic import BaseModel, EmailStr
from typing import Optional
from . import auth

class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class Usuario(UsuarioBase):
    id: int
    es_activo: bool
    es_admin: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    cantidad: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    estado: str

    class Config:
        orm_mode = True
