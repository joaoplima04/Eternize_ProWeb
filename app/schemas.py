from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum

class Categoria(str, Enum):
    PRATO_RASO = "Prato Raso"
    GUARDANAPO = "Guardanapo"
    TALHER = "Talher"
    TACAS = "Tacas"
    TRILHOS_DE_MESA = "Trilhos de Mesa"
    SOUSPLAT = "Sousplat"
    JOGO_AMERICANO = "Jogo Americano"
    CHA_E_CAFE = "Cha e Cafe"
    PRATO_SOBREMESA = "Prato Sobremesa"
    PORTA_GUARDANAPO = "Porta Guardanapo"

class Estilo(str, Enum):
    ELEGANTE = "Elegante"
    TROPICAL = "Tropical"
    FLORIDO = "Florido"

class ProdutoBase(BaseModel):
    nome: str
    categoria: str
    preco: float
    quantidade_estoque: int
    imagem: Optional[str] = None
    cor: str
    estilo: str
    publicado: bool

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int

    class Config:
        orm_mode = True

class ClienteBase(BaseModel):
    cpf: str
    nome: str
    email: str
    telefone: str
    data_nascimento: date

class ClienteCreate(ClienteBase):
    password: str

class Cliente(ClienteBase):
    class Config:
        orm_mode = True

class AluguelBase(BaseModel):
    cliente_cpf: str
    data_aluguel: date
    hora_inicial: str
    data_devolucao: date
    hora_final: str
    preco_total: float
    tipo_entrega: str

class AluguelCreate(AluguelBase):
    pass

class Aluguel(AluguelBase):
    id: int

    class Config:
        orm_mode = True

class EntregaBase(BaseModel):
    cep: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    nome_destinatario: Optional[str] = None

class EntregaCreate(EntregaBase):
    aluguel_id: int

    def to_dict(self):
        return self.dict()   

class Entrega(EntregaBase):
    id: int
    aluguel_id: int

    class Config:
        orm_mode = True
