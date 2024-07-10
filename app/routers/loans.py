from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import schemas, crud, auth
from ..database import get_db
from ..config import templates
from fastapi import Form
from typing import Optional
from .. import schemas  # Ajuste o caminho conforme necessário


router = APIRouter()

def get_aluguel_form(
    cliente_cpf: str = Form(...),
    data_aluguel: str = Form(...),
    hora_inicial: str = Form(...),
    data_devolucao: str = Form(...),
    hora_final: str = Form(...),
    preco_total: float = Form(...),
    tipo_entrega: Optional[str] = Form(None),
    cep: Optional[str] = Form(None),
    endereco: Optional[str] = Form(None),
    bairro: Optional[str] = Form(None),
    cidade: Optional[str] = Form(None),
    numero: Optional[str] = Form(None),
    complemento: Optional[str] = Form(None),
    nome_destinatario: Optional[str] = Form(None),
) -> schemas.AluguelCreate:
    entrega = schemas.EntregaCreate(
        tipo_entrega=tipo_entrega,
        cep=cep,
        endereco=endereco,
        bairro=bairro,
        cidade=cidade,
        numero=numero,
        complemento=complemento,
        nome_destinatario=nome_destinatario,
    ) if tipo_entrega == "Frete" else None

    return schemas.AluguelCreate(
        cliente_cpf=cliente_cpf,
        data_aluguel=data_aluguel,
        hora_inicial=hora_inicial,
        data_devolucao=data_devolucao,
        hora_final=hora_final,
        preco_total=preco_total,
        entrega=entrega
    )


@router.post("/locacao/", response_model=schemas.Aluguel)
def create_locacao(aluguel: schemas.AluguelCreate = Depends(get_aluguel_form), db: Session = Depends(get_db)):
    # Verificar se o cliente existe
    cliente = crud.get_cliente(db, cliente_cpf=aluguel.cliente_cpf)
    if not cliente:
        raise HTTPException(status_code=400, detail="Cliente não encontrado")

    # Criar a locação sem o preço total
    new_aluguel = crud.create_aluguel(db=db, aluguel=aluguel)

    # Calcular o preço total do carrinho
    cart_total = crud.get_cart_total(db, aluguel_id=new_aluguel.id)
    
    # Atualizar o preço total na locação
    new_aluguel.preco_total = cart_total
    db.commit()
    db.refresh(new_aluguel)

    # Adicionar a entrega, se necessário
    if aluguel.entrega:
        entrega_data = aluguel.entrega.dict()
        entrega_data['aluguel_id'] = new_aluguel.id
        crud.create_entrega(db=db, entrega=schemas.EntregaCreate(**entrega_data))

    return RedirectResponse()