from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response, JSONResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Produto, ItemCarrinho
from ..config import templates
from .. import auth

router = APIRouter()

# View do carrinho
@router.get("/", response_class=HTMLResponse)
def cart_view(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    user = None
    if token:
        try:
            user = auth.get_current_user(token, db)
        except HTTPException as e:
            # Trate a exceção se o token estiver presente, mas for inválido
            raise HTTPException(status_code=e.status_code, detail=f"Problema de autenticação: {e.detail}")

    if not user:
        context = {
            "type": "1",
            "message": "Para acessar o carrinho é preciso estar logado.",
            "request": request
        }
        return templates.TemplateResponse("categorias/login.html", context)
    cart_items = db.query(ItemCarrinho).all()
    return templates.TemplateResponse("categorias/carrinho.html", {"request": request, "cart_items": cart_items})

# Adicionar ao carrinho
@router.post("/add_to_cart/{produto_id}/")
def add_to_cart_endpoint(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    item_carrinho = db.query(ItemCarrinho).filter(ItemCarrinho.produto_id == produto_id).first()
    if item_carrinho:
        item_carrinho.quantidade += 1
    else:
        new_item = ItemCarrinho(produto_id=produto_id, quantidade=1)
        db.add(new_item)
    db.commit()
    
    return Response(status_code=200)

# Remover do carrinho
@router.post("/remove_from_cart/{produto_id}/")
def remove_from_cart_endpoint(produto_id: int, db: Session = Depends(get_db)):
    item_carrinho = db.query(ItemCarrinho).filter(ItemCarrinho.produto_id == produto_id).first()
    if not item_carrinho:
        raise HTTPException(status_code=404, detail="Item do carrinho não encontrado")

    db.delete(item_carrinho)
    db.commit()
    return Response(status_code=200)

@router.get("/cart_total/")
def get_cart_total(db: Session = Depends(get_db)):
    cart_items = db.query(ItemCarrinho).filter_by().all()
    cart_total = sum(item.produto.preco * item.quantidade for item in cart_items)
    return {"cart_total": cart_total}

# Atualizar quantidade
@router.post("/update_quantity/{produto_id}/{quantity}")
def update_quantity_endpoint(produto_id: int, quantity: int, db: Session = Depends(get_db)):
    item_carrinho = db.query(ItemCarrinho).filter(ItemCarrinho.produto_id == produto_id).first()
    if not item_carrinho:
        raise HTTPException(status_code=404, detail="Item do carrinho não encontrado")

    if quantity <= 0:
        db.delete(item_carrinho)
    else:
        item_carrinho.quantidade = quantity

    db.commit()
    return Response(status_code=200)
