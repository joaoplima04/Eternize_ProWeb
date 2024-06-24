from sqlalchemy.orm import Session
from sqlalchemy import update

from .database import get_db, SessionLocal
from .models import Produto

def prepend_static_to_image_paths():
    # Obtenha uma sessão do banco de dados
    db: Session = SessionLocal()
    
    try:
        # Obtenha todos os produtos
        produtos = db.query(Produto).all()
        
        # Atualize o campo imagem de cada produto
        for produto in produtos:
            produto.imagem = str(produto.imagem).replace("imagens", "images")
        
        db.commit()  # Confirme as alterações no banco de dados
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        db.rollback()  # Reverte a transação em caso de erro
    finally:
        db.close()  # Feche a sessão do banco de dados

if __name__ == "__main__":
    prepend_static_to_image_paths()
