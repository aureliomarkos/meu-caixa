from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Sale)
def create_sale(
    *,
    db: Session = Depends(get_db),
    sale_in: schemas.SaleCreate,
) -> Any:
    items_data = sale_in.itens
    sale_data = sale_in.dict(exclude={"itens", "valor_entrada"})
    valor_entrada_manual = sale_in.valor_entrada
    
    # Se o valor total não foi enviado, calculamos com base nos itens
    total_calculado = 0
    itens_processados = []
    
    if items_data:
        for item in items_data:
            # Busca o produto para garantir que existe e pegar o preço se necessário
            product = db.query(models.Product).filter(models.Product.id_produto == item.id_produto).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Produto com ID {item.id_produto} não encontrado")
            
            # Usa o valor enviado ou o preço atual do produto
            v_unitario = item.valor_unitario if item.valor_unitario is not None else product.preco_venda
            subtotal = item.qtde * v_unitario
            total_calculado += subtotal
            
            itens_processados.append({
                "id_produto": item.id_produto,
                "qtde": item.qtde,
                "valor_unitario": v_unitario,
                "subtotal": subtotal
            })

    # Se valor_total for None ou 0, usa o calculado
    final_total = sale_data.get("valor_total") or total_calculado
    sale_data["valor_total"] = final_total

    sale = models.Sale(**sale_data)
    db.add(sale)
    db.commit()
    db.refresh(sale)
    
    for item_data in itens_processados:
        db_item = models.SaleItem(
            id_vendas=sale.id_vendas,
            **item_data
        )
        db.add(db_item)

    # Lógica de Pagamento Inicial
    amount_to_record = 0
    if sale.status_pagamento == models.StatusPagamento.pago:
        amount_to_record = final_total
    elif valor_entrada_manual and valor_entrada_manual > 0:
        amount_to_record = valor_entrada_manual

    if amount_to_record > 0:
        db_payment = models.SalePayment(
            id_vendas=sale.id_vendas,
            valor_pago=amount_to_record,
            forma_pagamento=sale.forma_pagamento,
            observacao="Pagamento inicial / Entrada"
        )
        db.add(db_payment)
    
    db.commit()
    db.refresh(sale)
    return sale

@router.put("/{sale_id}", response_model=schemas.Sale)
def update_sale(
    *,
    db: Session = Depends(get_db),
    sale_id: int,
    sale_in: schemas.SaleCreate,
) -> Any:
    db_sale = db.query(models.Sale).filter(models.Sale.id_vendas == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Update main sale data
    update_data = sale_in.dict(exclude={"itens"}, exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sale, field, value)
    
    # Drop old items and recreate (simplest way for updates)
    db.query(models.SaleItem).filter(models.SaleItem.id_vendas == sale_id).delete()
    
    total_calculado = 0
    if sale_in.itens:
        for item in sale_in.itens:
            product = db.query(models.Product).filter(models.Product.id_produto == item.id_produto).first()
            v_unitario = item.valor_unitario if item.valor_unitario is not None else (product.preco_venda if product else 0)
            subtotal = item.qtde * v_unitario
            total_calculado += subtotal
            
            db_item = models.SaleItem(
                id_vendas=sale_id,
                id_produto=item.id_produto,
                qtde=item.qtde,
                valor_unitario=v_unitario,
                subtotal=subtotal
            )
            db.add(db_item)
            
    # Update total if not provided
    if not sale_in.valor_total:
        db_sale.valor_total = total_calculado
        
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale
@router.get("/", response_model=List[schemas.Sale])
def read_sales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    sales = db.query(models.Sale).offset(skip).limit(limit).all()
    return sales

@router.get("/{sale_id}", response_model=schemas.Sale)
def read_sale(
    *,
    db: Session = Depends(get_db),
    sale_id: int,
) -> Any:
    sale = db.query(models.Sale).filter(models.Sale.id_vendas == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@router.delete("/{sale_id}")
def delete_sale(
    *,
    db: Session = Depends(get_db),
    sale_id: int,
) -> Any:
    sale = db.query(models.Sale).filter(models.Sale.id_vendas == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    db.query(models.SaleItem).filter(models.SaleItem.id_vendas == sale_id).delete()
    db.query(models.SalePayment).filter(models.SalePayment.id_vendas == sale_id).delete()
    db.delete(sale)
    db.commit()
    return {"message": "Sale deleted successfully"}

# Payments
@router.post("/{sale_id}/payments", response_model=schemas.SalePayment)
def create_payment(
    *,
    db: Session = Depends(get_db),
    sale_id: int,
    payment_in: schemas.SalePaymentCreate,
) -> Any:
    sale = db.query(models.Sale).filter(models.Sale.id_vendas == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    db_payment = models.SalePayment(
        **payment_in.dict(),
        id_vendas=sale_id
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.delete("/payments/{payment_id}")
def delete_payment(
    *,
    db: Session = Depends(get_db),
    payment_id: int,
) -> Any:
    payment = db.query(models.SalePayment).filter(models.SalePayment.id_venda_pagamento == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    db_delete = payment
    db.delete(payment)
    db.commit()
    return {"message": "Payment deleted successfully"}

@router.post("/batch-payment/{client_id}")
def batch_payment_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    payment_in: schemas.BatchPaymentRequest,
) -> Any:
    # 1. Buscar todas as vendas não quitadas do cliente, ordenadas por data (mais antigas primeiro)
    sales = db.query(models.Sale).filter(
        models.Sale.id_cliente == client_id,
        models.Sale.status_pagamento != models.StatusPagamento.pago
    ).order_by(models.Sale.data_venda.asc()).all()

    if not sales:
        raise HTTPException(status_code=404, detail="Nenhuma venda em aberto encontrada para este cliente")

    total_to_distribute = payment_in.valor_total
    payments_made = []

    for sale in sales:
        if total_to_distribute <= 0:
            break

        # Calcular saldo devedor da venda
        total_paid_on_sale = sum([p.valor_pago for p in sale.pagamentos])
        current_debt = sale.valor_total - total_paid_on_sale

        if current_debt <= 0:
            continue

        # Quanto podemos pagar nesta nota agora?
        amount_to_pay = min(current_debt, total_to_distribute)

        # Registrar o pagamento
        db_payment = models.SalePayment(
            id_vendas=sale.id_vendas,
            valor_pago=amount_to_pay,
            forma_pagamento=payment_in.forma_pagamento,
            observacao=payment_in.observacao
        )
        db.add(db_payment)
        
        # Atualizar status da venda
        new_total_paid = total_paid_on_sale + amount_to_pay
        if new_total_paid >= sale.valor_total:
            sale.status_pagamento = models.StatusPagamento.pago
        else:
            sale.status_pagamento = models.StatusPagamento.parcial
        
        db.add(sale)
        total_to_distribute -= amount_to_pay
        payments_made.append({"sale_id": sale.id_vendas, "amount": amount_to_pay})

    db.commit()
    return {
        "message": f"Processado recebimento de {payment_in.valor_total}",
        "distributed_amount": payment_in.valor_total - total_to_distribute,
        "remaining_credit": total_to_distribute,
        "affected_sales": payments_made
    }
