import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import models, crud

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_get_preco_unitario(db):
    # Criação de um produto de teste
    produto = models.Produto(id=1, nome="Produto Teste", preco=100.0)
    db.add(produto)
    db.commit()
    db.refresh(produto)

    # Teste da função get_preco_unitario
    preco = crud.get_preco_unitario(db, produto_id=produto.id)
    assert preco == 100.0

def test_get_cart_total(db):
    # Criação de produtos de teste
    produto1 = models.Produto(id=1, nome="Produto Teste 1", preco=100.0)
    produto2 = models.Produto(id=2, nome="Produto Teste 2", preco=200.0)
    db.add(produto1)
    db.add(produto2)
    db.commit()
    db.refresh(produto1)
    db.refresh(produto2)

    # Criação de itens no carrinho
    item1 = models.ItemCarrinho(id=1, produto_id=produto1.id, quantidade=2, aluguel_id=1)
    item2 = models.ItemCarrinho(id=2, produto_id=produto2.id, quantidade=1, aluguel_id=1)
    db.add(item1)
    db.add(item2)
    db.commit()
    db.refresh(item1)
    db.refresh(item2)

    # Teste da função get_cart_total
    total = crud.get_cart_total(db, aluguel_id=1)
    assert total == 400.0  # (2 * 100.0) + (1 * 200.0)
