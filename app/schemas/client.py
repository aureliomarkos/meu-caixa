from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class ClientBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    limite_credito: Optional[Decimal] = 0.00

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id_cliente: int
    data_cadastro: Optional[datetime] = None
    saldo_devedor: Optional[Decimal] = 0.00

    class Config:
        from_attributes = True
