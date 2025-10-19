from fastapi import APIRouter

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

@router.get("/")
def leer_usuarios():
    return {"mensaje": "Aquí irán los usuarios"}
