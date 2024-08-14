from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from . import crud
from sqlalchemy.orm import Session
from fastapi import Depends
from .database import get_db

def gerar_contrato(aluguel_id, db: Session = Depends(get_db)):
    # Configurar Jinja2 para carregar o template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('contrato_template.html')

    aluguel = crud.get_aluguel(db, aluguel_id)

    # Renderizar o template com os dados do contrato
    html_content = template.render(
        cliente_nome=aluguel.cliente,
        cliente_cpf_cnpj=aluguel.cliente_cpf,
        cliente_telefone=aluguel.cliente.telefone,
        data_pedido=aluguel,
        data_confirmacao=aluguel,
        inicio_locacao=aluguel,
        termino_locacao=aluguel,
        objetivo_locacao=aluguel,
        data_entrega=aluguel,
        hora_entrega=aluguel,
        data_devolucao=aluguel,
        hora_devolucao=aluguel,
        itens=itens,
        data_contrato=aluguel
    )

    # Gerar o PDF
    pdf = HTML(string=html_content).write_pdf()
    with open(f'contrato_{pedido["numero"]}.pdf', 'wb') as f:
        f.write(pdf)