from fastapi import APIRouter, Depends, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..models import Produto, ItemCarrinho
from ..config import templates
from .. import schemas, crud

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def admin_view(request: Request):
    return templates.TemplateResponse("admin/base.html", context={"request":request})

@router.get("/add_produto", response_class=HTMLResponse)
def admin_view(request: Request):
    return templates.TemplateResponse("admin/produtoForms.html", context={"request":request})

def get_produto_form(
    nome: str = Form(...),
    categoria: schemas.Categoria = Form(...),
    preco: float = Form(...),
    quantidade_estoque: int = Form(...),
    imagem: UploadFile = File(None),
    cor: str = Form(...),
    estilo: schemas.Estilo = Form(...),
    publicado: bool = Form(...),    
) -> schemas.ProdutoCreate:
    if imagem:
        imagem_path = f"static/images/{imagem.filename}"
        with open(imagem_path, "wb") as buffer:
            buffer.write(imagem.file.read())
    else:
        imagem_path = None

    return schemas.ProdutoCreate(
        nome=nome,
        categoria=categoria,
        preco=preco,
        quantidade_estoque=quantidade_estoque,
        imagem=imagem_path,
        cor=cor,
        estilo=estilo,
        publicado=publicado
    )

@router.post("/cadastro_produto/", respose_model=schemas.Produto)
def create_produto(produto: schemas.ProdutoCreate = Depends(get_produto_form), db: Session = Depends(get_db)):
    crud.create_produto(db=db, produto=produto)

    response = RedirectResponse(url="/add_produto" , status_code=303)

    response.set_cookie(key="admin_message", value="Produto adicionado com sucesso!", expires=timedelta(seconds=30))

    return response


