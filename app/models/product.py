from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Category(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    produtos = relationship("Product", back_populates="categoria")

class Product(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    id_categoria = Column(Integer, ForeignKey("categorias.id_categoria"))
    preco_custo = Column(DECIMAL(10, 2))
    preco_venda = Column(DECIMAL(10, 2), nullable=False)

    categoria = relationship("Category", back_populates="produtos")
