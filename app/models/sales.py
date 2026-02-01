from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, TIMESTAMP, Enum, func, String
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class StatusPagamento(str, enum.Enum):
    pendente = 'Pendente'
    pago = 'Pago'
    parcial = 'Parcial'

class FormaPagamento(str, enum.Enum):
    dinheiro = 'Dinheiro'
    cartao_debito = 'Cartão Débito'
    cartao_credito = 'Cartão Crédito'
    pix = 'Pix'

class Sale(Base):
    __tablename__ = "vendas"

    id_vendas = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    data_venda = Column(TIMESTAMP, server_default=func.now())
    status_pagamento = Column(Enum(StatusPagamento), default=StatusPagamento.pendente)
    forma_pagamento = Column(Enum(FormaPagamento), nullable=True) # Pode ser null se pendente? Schema doesn't say NOT NULL
    valor_total = Column(DECIMAL(10, 2))

    itens = relationship("SaleItem", back_populates="venda")
    pagamentos = relationship("SalePayment", back_populates="venda")

class SalePayment(Base):
    __tablename__ = "venda_pagamentos"

    id_venda_pagamento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_vendas = Column(Integer, ForeignKey("vendas.id_vendas"))
    data_pagamento = Column(TIMESTAMP, server_default=func.now())
    valor_pago = Column(DECIMAL(10, 2))
    forma_pagamento = Column(Enum(FormaPagamento))
    observacao = Column(String(255), nullable=True)

    venda = relationship("Sale", back_populates="pagamentos")
    # Add relationship to client if needed later, but Client model wasn't updated with back_populates yet.

class SaleItem(Base):
    __tablename__ = "venda_itens"

    id_venda_item = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_vendas = Column(Integer, ForeignKey("vendas.id_vendas"))
    id_produto = Column(Integer, ForeignKey("produtos.id_produto"))
    qtde = Column(DECIMAL(10, 2))
    valor_unitario = Column(DECIMAL(10, 2))
    subtotal = Column(DECIMAL(10, 2))

    venda = relationship("Sale", back_populates="itens")
    # Product relationship
    produto = relationship("app.models.product.Product")
