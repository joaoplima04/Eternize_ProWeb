from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, Request, Form, UploadFile
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..models import Produto, ItemCarrinho, Aluguel
from ..config import templates
from .. import schemas, crud
from jinja2 import Environment
from datetime import datetime
import boto3

s3 = boto3.client('s3')

def upload_file_to_s3(file: UploadFile, bucket_name: str, key: str):
    # Carregar o arquivo para o bucket S3
    s3.upload_fileobj(file.file, bucket_name, key)
    
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def admin_view(request: Request):
    return templates.TemplateResponse("admin/base.html", context={"request":request})

@router.get("/add_produto", response_class=HTMLResponse)
def cadastro_produto_view(request: Request):
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
        # Defina o nome do bucket e o caminho onde a imagem será armazenada no S3
        bucket_name = "eternize-bucket"
        imagem_path = f"imagens/{imagem.filename}"
        
        # Faça o upload da imagem para o S3
        upload_file_to_s3(imagem, bucket_name, imagem_path)

        # Monta a URL completa da imagem
        imagem_url = f"https://{bucket_name}.s3.amazonaws.com/{imagem_path}"
    else:
        imagem_path = None

    return schemas.ProdutoCreate(
        nome=nome,
        categoria=categoria,
        preco=preco,
        quantidade_estoque=quantidade_estoque,
        imagem=imagem_url,
        cor=cor,
        estilo=estilo,
        publicado=publicado
    )

@router.post("/cadastro_produto/")
def create_produto(produto: schemas.ProdutoCreate = Depends(get_produto_form), db: Session = Depends(get_db)):
    crud.create_produto(db=db, produto=produto)

    response = RedirectResponse(url="/admin/add_produto" , status_code=303)

    response.set_cookie(key="admin_message", value="Produto adicionado com sucesso!", expires=timedelta(seconds=30))

    return response

@router.get("/produtos/", response_model=List[schemas.Produto])
def read_produtos(categoria: str = '', db: Session = Depends(get_db)):
    if categoria:
        produtos = db.query(Produto).filter(Produto.categoria == categoria).all()
    else:
        produtos = db.query(Produto).all()
    return produtos

@router.get("/visualizar_produtos/", response_class=HTMLResponse)
def visualizar_produtos(request: Request):
    return templates.TemplateResponse("admin/produtos.html", {"request": request})

@router.get("/editar_produto/{produto_id}", response_class=HTMLResponse)
async def editar_produto(request: Request, produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    return templates.TemplateResponse("admin/editar_produto.html", {"request": request, "produto": produto})

@router.put("/produtos/{produto_id}")
def update_produto(produto_id: int, produto: schemas.ProdutoCreate, db: Session = Depends(get_db), file: UploadFile = File(None)):
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for key, value in produto.dict().items():
        setattr(db_produto, key, value)

    if file:
        file_location = f"/static/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        db_produto.imagem = file.filename

    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.get("/visualizar_locacoes/")
def visualizar_locacoes(request: Request, db: Session = Depends(get_db)):
    locacoes = db.query(Aluguel).all()
     
    return templates.TemplateResponse("admin/locacoes.html", {"request": request, "locacoes": locacoes})

#Filtro date
def format_date(value, format="%d %b %Y %H:%M"):
    return value.strftime(format)

#Filtro Time
def format_time(value, format="%H:%M"):
    return value.strftime(format)

# Adicione os filtros ao ambiente do Jinja2
templates.env.filters['format_date'] = format_date
templates.env.filters['format_time'] = format_time