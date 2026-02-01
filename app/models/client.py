from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, func
from app.core.database import Base

class Client(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20))
    email = Column(String(255))
    limite_credito = Column(DECIMAL(10, 2), default=0.00)
    data_cadastro = Column(TIMESTAMP, server_default=func.now())
