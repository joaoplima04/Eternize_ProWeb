from sqlalchemy.orm import Session
from . import models, schemas
import shutil
from fastapi import UploadFile
from .auth import get_password_hash

# Funções CRUD para o modelo Produto

def get_produto(db: Session, produto_id: int):
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first()

def get_produtos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Produto).offset(skip).limit(limit).all()


def create_produto(db: Session, produto: schemas.ProdutoCreate, imagem: UploadFile = None):
    db_produto = models.Produto(**produto.dict())
    
    if imagem:
        file_location = f"static/images/{imagem.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(imagem.file, file_object)
        db_produto.imagem = file_location

    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

# Funções CRUD para o modelo Cliente

def get_cliente(db: Session, cliente_email: str):
    return db.query(models.Cliente).filter(models.Cliente.email == cliente_email).first()

def get_clientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    # Hashear a senha antes de salvar
    hashed_password = get_password_hash(cliente.password)
    db_cliente = models.Cliente(
        cpf=cliente.cpf,
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone,
        data_nascimento=cliente.data_nascimento,
        password=hashed_password  # Armazenar a senha hasheada
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Funções CRUD para o modelo Aluguel

def get_aluguel(db: Session, aluguel_id: int):
    return db.query(models.Aluguel).filter(models.Aluguel.id == aluguel_id).first()

def get_alugueis(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Aluguel).offset(skip).limit(limit).all()

def create_aluguel(db: Session, aluguel: schemas.AluguelCreate):
    db_aluguel = models.Aluguel(**aluguel.dict())
    db.add(db_aluguel)
    db.commit()
    db.refresh(db_aluguel)
    return db_aluguel

def create_entrega(db: Session, entrega: schemas.EntregaCreate):
    db_entrega = models.Entrega(**entrega.dict())
    db.add(db_entrega)
    db.commit()
    db.refresh(db_entrega)
    return db_entrega

def get_entrega(db: Session, entrega_id: int):
    return db.query(models.Entrega).filter(models.Entrega.id == entrega_id).first()

def get_cart_total(db: Session, aluguel_id: int) -> float:
    cart_items = db.query(models.ItemCarrinho).filter_by(aluguel_id=aluguel_id).all()
    cart_total = sum(item.produto.preco * item.quantidade for item in cart_items)
    return cart_total