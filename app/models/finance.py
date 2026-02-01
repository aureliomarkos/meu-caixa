from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DATE, TIMESTAMP, Enum, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class TipoAdiantamento(str, enum.Enum):
    adiantamento = 'Adiantamento'
    vale = 'Vale'
    salario = 'Salário'
    bonus = 'Bônus'
    outros = 'Outros'

class StatusConta(str, enum.Enum):
    a_vencer = 'A Vencer'
    pago = 'Pago'
    atrasado = 'Atrasado'

class Supplier(Base):
    __tablename__ = "fornecedores"

    id_fornecedor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20))
    contato = Column(String(50))

    contas_pagar = relationship("AccountsPayable", back_populates="fornecedor")

class Employee(Base):
    __tablename__ = "funcionarios"

    id_funcionario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20))
    salario = Column(DECIMAL(10, 2), nullable=False)
    data_admissao = Column(DATE)

    adiantamentos = relationship("Advance", back_populates="funcionario")

class Advance(Base):
    __tablename__ = "adiantamentos"

    id_lancamento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_funcionario = Column(Integer, ForeignKey("funcionarios.id_funcionario"))
    tipo = Column(Enum(TipoAdiantamento), default=TipoAdiantamento.adiantamento, nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)
    data_registro = Column(TIMESTAMP, server_default=func.now())
    mes_referencia = Column(String(7))

    funcionario = relationship("Employee", back_populates="adiantamentos")

class AccountsPayable(Base):
    __tablename__ = "contas_pagar"

    id_contas_pagar = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_fornecedor = Column(Integer, ForeignKey("fornecedores.id_fornecedor"))
    numero_nota = Column(String(50))
    data_vencimento = Column(DATE, nullable=False)
    valor_total_nota = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(StatusConta), default=StatusConta.a_vencer)

    fornecedor = relationship("Supplier", back_populates="contas_pagar")
    itens = relationship("AccountsPayableItem", back_populates="conta_pagar")

class AccountsPayableItem(Base):
    __tablename__ = "contas_pagar_itens"

    id_contas_pagar_item = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_contas_pagar = Column(Integer, ForeignKey("contas_pagar.id_contas_pagar"))
    descricao_item = Column(String(100))
    qtde = Column(DECIMAL(10, 2))
    valor_unitario = Column(DECIMAL(10, 2))

    conta_pagar = relationship("AccountsPayable", back_populates="itens")
