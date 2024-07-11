from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from fastapi import Form
from typing import Optional
from .. import schemas 

router = APIRouter()


def get_aluguel_form(
    request: Request,
    data_aluguel: str = Form(...),
    hora_inicial: str = Form(...),
    data_devolucao: str = Form(...),
    hora_final: str = Form(...),
    tipo_entrega: str = Form(...),
    cep: Optional[str] = Form(None),
    endereco: Optional[str] = Form(None),
    bairro: Optional[str] = Form(None),
    cidade: Optional[str] = Form(None),
    numero: Optional[str] = Form(None),
    complemento: Optional[str] = Form(None),
    nome_destinatario: Optional[str] = Form(None),
) -> tuple:
    if tipo_entrega == "Frete":
        entrega = schemas.EntregaCreate(
            aluguel_id=0,
            cep=cep,
            endereco=endereco,
            bairro=bairro,
            cidade=cidade,
            numero=numero,
            complemento=complemento,
            nome_destinatario=nome_destinatario,
        )
    else:
        entrega = None

    aluguel = schemas.AluguelCreate(
        cliente_cpf=request.cookies.get("cpf"),
        data_aluguel=data_aluguel,
        hora_inicial=hora_inicial,
        data_devolucao=data_devolucao,
        hora_final=hora_final,
        preco_total=0,
        tipo_entrega=tipo_entrega,
    )

    return aluguel, entrega


@router.post("/locacao/", response_class=RedirectResponse)
def create_locacao(retorno = Depends(get_aluguel_form), db: Session = Depends(get_db)):
    
    aluguel: schemas.AluguelCreate = retorno[0]

    entrega: schemas.EntregaCreate = retorno[1]

    # Verificar se o cliente existe
    cliente = crud.get_cliente(db, cliente_cpf=aluguel.cliente_cpf)
    if not cliente:
        raise HTTPException(status_code=400, detail="Cliente não encontrado")

    # Criar a locação sem o preço total
    new_aluguel = crud.create_aluguel(db=db, aluguel=aluguel)

    # Calcular o preço total do carrinho
    cart_total = crud.get_cart_total(db, cliente_cpf=cliente.cpf)
    
    # Atualizar o preço total na locação
    new_aluguel.preco_total = cart_total
    db.commit()
    db.refresh(new_aluguel)

    # Adicionar a entrega, se necessário

    if entrega is not None:
        entrega_data = entrega.dict()
        entrega_data['aluguel_id'] = new_aluguel.id
        crud.create_entrega(db=db, entrega=schemas.EntregaCreate(**entrega_data))

    cart_items = crud.get_cart_items(db, cliente_cpf=cliente.cpf)
    for item in cart_items:
        item.aluguel_id = new_aluguel.id
        db.commit()
        db.refresh(item)

    return RedirectResponse("/", status_code=303)