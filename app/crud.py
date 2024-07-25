from sqlalchemy.orm import Session
from . import models, schemas
import shutil
from fastapi import UploadFile, Request
from .auth import get_password_hash

# Funções CRUD para o modelo Produto

def get_produto(db: Session, produto_id: int):
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first()

def get_produtos(db: Session, skip: int = 0):
    return db.query(models.Produto).offset(skip).all()


def create_produto(db: Session, produto: schemas.ProdutoCreate, imagem: UploadFile = None):
    db_produto = models.Produto(**produto.dict())
    
    if imagem:
        file_location = f"static/imagens/{imagem.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(imagem.file, file_object)
        db_produto.imagem = file_location

    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

# Funções CRUD para o modelo Cliente

def get_cliente(db: Session, cliente_cpf: str):
    return db.query(models.Cliente).filter(models.Cliente.cpf == cliente_cpf).first()

def get_cliente_by_email(db: Session, cliente_email: str):
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

# Entrega

def create_entrega(db: Session, entrega: schemas.EntregaCreate):
    db_entrega = models.Entrega(**entrega.dict())
    db.add(db_entrega)
    db.commit()
    db.refresh(db_entrega)
    return db_entrega

def get_entrega(db: Session, entrega_id: int):
    return db.query(models.Entrega).filter(models.Entrega.id == entrega_id).first()

# Carrinho / ItemCarrinho

def get_preco_unitario(db: Session, produto_id: int) -> float:
    produto = db.query(models.Produto).filter_by(id=produto_id).first()
    return produto.preco

'''
def create_cart_item(db: Session, produto_id: int, request: Request):
    cliente_cpf = request.cookies.get("cpf")
    novo_item = models.ItemCarrinho(produto_id=produto_id, quantidade=1, cliente_cpf=cliente_cpf)
    db.add(novo_item)
    db.commit()
'''

def get_cart_items(db: Session, cliente_cpf: str):
    return db.query(models.ItemCarrinho).filter(models.ItemCarrinho.cliente_cpf == cliente_cpf, models.ItemCarrinho.aluguel_id == None).all()

def get_cart_total(db: Session, cliente_cpf: str) -> float:
    cart_items = get_cart_items(db=db, cliente_cpf=cliente_cpf)
    cart_total = sum(get_preco_unitario(db=db, produto_id=item.produto_id) * item.quantidade for item in cart_items)
    return cart_total

def clear_cart(db: Session, aluguel_id: int):
    db.query(models.ItemCarrinho).filter(models.ItemCarrinho.aluguel_id == aluguel_id).delete()
    db.commit()

