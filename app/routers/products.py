from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app import schemas, crud
from ..database import get_db

router = APIRouter()

# Rota para criar um novo produto
@router.post("/cadastro/", response_model=schemas.Produto)
def create_produto(
    produto: schemas.ProdutoCreate, 
    db: Session = Depends(get_db), 
    imagem: UploadFile = File(None)
):
    return crud.create_produto(db=db, produto=produto, imagem=imagem)