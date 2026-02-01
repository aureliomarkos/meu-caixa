from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from app.models.sales import StatusPagamento, FormaPagamento
from app.schemas.product import Product

class SaleItemBase(BaseModel):
    id_produto: int
    qtde: Decimal
    valor_unitario: Optional[Decimal] = None # Can be fetched from product if not provided, but mostly input
    subtotal: Optional[Decimal] = None

class SaleItemCreate(SaleItemBase):
    pass

class SaleItem(SaleItemBase):
    id_venda_item: int
    id_vendas: int
    produto: Optional[Product] = None

    class Config:
        from_attributes = True

class SalePaymentBase(BaseModel):
    valor_pago: Decimal
    forma_pagamento: FormaPagamento
    observacao: Optional[str] = None

class SalePaymentCreate(SalePaymentBase):
    pass

class SalePayment(SalePaymentBase):
    id_venda_pagamento: int
    id_vendas: int
    data_pagamento: datetime

    class Config:
        from_attributes = True

class BatchPaymentRequest(BaseModel):
    valor_total: Decimal
    forma_pagamento: FormaPagamento
    observacao: Optional[str] = "Baixa Automática (FIFO)"

class SaleBase(BaseModel):
    id_cliente: Optional[int] = None
    status_pagamento: StatusPagamento = StatusPagamento.pendente
    forma_pagamento: Optional[FormaPagamento] = None
    valor_total: Optional[Decimal] = None

class SaleCreate(SaleBase):
    itens: Optional[List[SaleItemCreate]] = []
    valor_entrada: Optional[Decimal] = None

class Sale(SaleBase):
    id_vendas: int
    data_venda: datetime
    itens: List[SaleItem] = []
    pagamentos: List[SalePayment] = []

    class Config:
        from_attributes = True
