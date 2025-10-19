from pydantic import BaseModel

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
