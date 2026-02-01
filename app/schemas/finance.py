from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime
from app.models.finance import TipoAdiantamento, StatusConta

# Supplier
class SupplierBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    contato: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id_fornecedor: int

    class Config:
        from_attributes = True

# Employee
class EmployeeBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    salario: Decimal
    data_admissao: Optional[date] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id_funcionario: int

    class Config:
        from_attributes = True

# Advance
class AdvanceBase(BaseModel):
    id_funcionario: int
    tipo: TipoAdiantamento = TipoAdiantamento.adiantamento
    valor: Decimal
    mes_referencia: Optional[str] = None

class AdvanceCreate(AdvanceBase):
    pass

class Advance(AdvanceBase):
    id_lancamento: int
    data_registro: datetime
    funcionario: Optional[Employee] = None

    class Config:
        from_attributes = True

# Accounts Payable
class AccountsPayableItemBase(BaseModel):
    descricao_item: Optional[str] = None
    qtde: Optional[Decimal] = None
    valor_unitario: Optional[Decimal] = None

class AccountsPayableItemCreate(AccountsPayableItemBase):
    pass

class AccountsPayableItem(AccountsPayableItemBase):
    id_contas_pagar_item: int
    id_contas_pagar: int

    class Config:
        from_attributes = True

class AccountsPayableBase(BaseModel):
    id_fornecedor: Optional[int] = None
    numero_nota: Optional[str] = None
    data_vencimento: date
    valor_total_nota: Decimal
    status: StatusConta = StatusConta.a_vencer

class AccountsPayableCreate(AccountsPayableBase):
    itens: Optional[List[AccountsPayableItemCreate]] = []

class AccountsPayable(AccountsPayableBase):
    id_contas_pagar: int
    fornecedor: Optional[Supplier] = None
    itens: List[AccountsPayableItem] = []

    class Config:
        from_attributes = True
