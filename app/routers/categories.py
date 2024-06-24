from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Produto
from ..config import templates

router = APIRouter()

@router.get("/categoria/{categoria_name}/", response_class=HTMLResponse)
def read_categoria(request: Request, categoria_name: str, db: Session = Depends(get_db)):
    # Implemente a lógica para filtrar produtos por categoria
    produtos = db.query(Produto).filter(Produto.categoria == categoria_name).all()
    return templates.TemplateResponse("categorias/categoria.html", {"request": request, "produtos": produtos, "categoria": categoria_name})
