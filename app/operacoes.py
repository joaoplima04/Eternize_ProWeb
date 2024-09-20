from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from .crud import get_aluguel, get_cart_items
from sqlalchemy.orm import Session
from fastapi import Depends
from .database import get_db, SessionLocal


def gerar_contrato(aluguel_id, db: Session = Depends(get_db)):
    # Configurar Jinja2 para carregar o template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/admin/contrato.html')

    aluguel = get_aluguel(db, aluguel_id)

    itens = aluguel.itens_carrinho

    # Renderizar o template com os dados do contrato
    html_content = template.render(
        cliente_nome=aluguel.cliente.nome,
        cliente_cpf_cnpj=aluguel.cliente_cpf,
        cliente_telefone=aluguel.cliente.telefone,
        data_pedido=aluguel.data_pedido,
        inicio_locacao=aluguel.data_aluguel,
        termino_locacao=aluguel.data_devolucao,
        objetivo_locacao=aluguel.objetivo,
        data_entrega=aluguel.data_devolucao,
        hora_entrega=aluguel.hora_final,
        data_devolucao=aluguel.data_devolucao,
        hora_devolucao=aluguel.hora_final,
        itens=itens,
        preco_total_pedido=aluguel.preco_total
    )

    # Gerar o PDF
    contrato_path = f'static/contratos/contrato_{aluguel.id}.pdf'
    HTML(string=html_content).write_pdf(contrato_path)
    
    return contrato_path






