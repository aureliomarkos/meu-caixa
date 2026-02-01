from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Client])
def read_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    clients = db.query(models.Client).offset(skip).limit(limit).all()
    
    # Calcular saldo devedor para cada cliente
    for client in clients:
        # Busca apenas as vendas que NÃO estão pagas
        sales = db.query(models.Sale).filter(
            models.Sale.id_cliente == client.id_cliente,
            models.Sale.status_pagamento != models.StatusPagamento.pago
        ).all()
        
        total_debt = 0
        for sale in sales:
            total_paid = sum([p.valor_pago for p in sale.pagamentos])
            total_debt += (sale.valor_total - total_paid)
            
        client.saldo_devedor = total_debt
        
    return clients

@router.post("/", response_model=schemas.Client)
def create_client(
    *,
    db: Session = Depends(get_db),
    client_in: schemas.ClientCreate,
) -> Any:
    client = models.Client(**client_in.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.put("/{client_id}", response_model=schemas.Client)
def update_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    client_in: schemas.ClientCreate,
) -> Any:
    client = db.query(models.Client).filter(models.Client.id_cliente == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    update_data = client_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)
    
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.delete("/{client_id}")
def delete_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
) -> Any:
    client = db.query(models.Client).filter(models.Client.id_cliente == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(client)
    db.commit()
    return {"message": "Client deleted successfully"}
