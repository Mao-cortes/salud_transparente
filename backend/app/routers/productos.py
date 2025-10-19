from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)

@router.post("/", response_model=schemas.Producto)
def crear_producto_endpoint(producto: schemas.ProductoCreate, db: Session = Depends(database.get_db)):
    return crud.crear_producto(db, producto)

@router.get("/", response_model=list[schemas.Producto])
def listar_productos(db: Session = Depends(database.get_db)):
    return crud.obtener_productos(db)
