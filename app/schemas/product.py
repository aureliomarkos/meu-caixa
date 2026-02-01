from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal

# Category
class CategoryBase(BaseModel):
    nome: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id_categoria: int

    class Config:
        from_attributes = True

# Product
class ProductBase(BaseModel):
    nome: str
    id_categoria: Optional[int] = None
    preco_custo: Optional[Decimal] = None
    preco_venda: Decimal

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id_produto: int
    categoria: Optional[Category] = None

    class Config:
        from_attributes = True
