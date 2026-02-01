from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.database import get_db

router = APIRouter()

# Suppliers
@router.post("/suppliers/", response_model=schemas.Supplier)
def create_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_in: schemas.SupplierCreate,
) -> Any:
    supplier = models.Supplier(**supplier_in.dict())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

@router.get("/suppliers/", response_model=List[schemas.Supplier])
def read_suppliers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    suppliers = db.query(models.Supplier).offset(skip).limit(limit).all()
    return suppliers

@router.put("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def update_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_id: int,
    supplier_in: schemas.SupplierCreate,
) -> Any:
    supplier = db.query(models.Supplier).filter(models.Supplier.id_fornecedor == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    update_data = supplier_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

@router.delete("/suppliers/{supplier_id}")
def delete_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_id: int,
) -> Any:
    supplier = db.query(models.Supplier).filter(models.Supplier.id_fornecedor == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    db.delete(supplier)
    db.commit()
    return {"message": "Supplier deleted successfully"}

# Employees
@router.post("/employees/", response_model=schemas.Employee)
def create_employee(
    *,
    db: Session = Depends(get_db),
    employee_in: schemas.EmployeeCreate,
) -> Any:
    employee = models.Employee(**employee_in.dict())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@router.get("/employees/", response_model=List[schemas.Employee])
def read_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    employees = db.query(models.Employee).offset(skip).limit(limit).all()
    return employees

@router.put("/employees/{employee_id}", response_model=schemas.Employee)
def update_employee(
    *,
    db: Session = Depends(get_db),
    employee_id: int,
    employee_in: schemas.EmployeeCreate,
) -> Any:
    employee = db.query(models.Employee).filter(models.Employee.id_funcionario == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = employee_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/employees/{employee_id}")
def delete_employee(
    *,
    db: Session = Depends(get_db),
    employee_id: int,
) -> Any:
    employee = db.query(models.Employee).filter(models.Employee.id_funcionario == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

# Advances
@router.post("/advances/", response_model=schemas.Advance)
def create_advance(
    *,
    db: Session = Depends(get_db),
    advance_in: schemas.AdvanceCreate,
) -> Any:
    advance = models.Advance(**advance_in.dict())
    db.add(advance)
    db.commit()
    db.refresh(advance)
    return advance

@router.get("/advances/", response_model=List[schemas.Advance])
def read_advances(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    advances = db.query(models.Advance).offset(skip).limit(limit).all()
    return advances

@router.put("/advances/{advance_id}", response_model=schemas.Advance)
def update_advance(
    *,
    db: Session = Depends(get_db),
    advance_id: int,
    advance_in: schemas.AdvanceCreate,
) -> Any:
    advance = db.query(models.Advance).filter(models.Advance.id_lancamento == advance_id).first()
    if not advance:
        raise HTTPException(status_code=404, detail="Advance not found")
    
    update_data = advance_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(advance, field, value)
    
    db.add(advance)
    db.commit()
    db.refresh(advance)
    return advance

@router.delete("/advances/{advance_id}")
def delete_advance(
    *,
    db: Session = Depends(get_db),
    advance_id: int,
) -> Any:
    advance = db.query(models.Advance).filter(models.Advance.id_lancamento == advance_id).first()
    if not advance:
        raise HTTPException(status_code=404, detail="Advance not found")
    
    db.delete(advance)
    db.commit()
    return {"message": "Advance deleted successfully"}

# Accounts Payable
@router.post("/accounts-payable/", response_model=schemas.AccountsPayable)
def create_accounts_payable(
    *,
    db: Session = Depends(get_db),
    ap_in: schemas.AccountsPayableCreate,
) -> Any:
    # Extract items to create separately
    items_data = ap_in.itens
    ap_data = ap_in.dict(exclude={"itens"})
    
    account = models.AccountsPayable(**ap_data)
    db.add(account)
    db.commit()
    db.refresh(account)
    
    if items_data:
        for item in items_data:
            db_item = models.AccountsPayableItem(
                **item.dict(),
                id_contas_pagar=account.id_contas_pagar
            )
            db.add(db_item)
        db.commit()
        db.refresh(account)

    return account

@router.get("/accounts-payable/", response_model=List[schemas.AccountsPayable])
def read_accounts_payable(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    accounts = db.query(models.AccountsPayable).offset(skip).limit(limit).all()
    return accounts

@router.get("/accounts-payable/{ap_id}", response_model=schemas.AccountsPayable)
def read_account_payable(
    *,
    db: Session = Depends(get_db),
    ap_id: int,
) -> Any:
    account = db.query(models.AccountsPayable).filter(models.AccountsPayable.id_contas_pagar == ap_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/accounts-payable/{ap_id}", response_model=schemas.AccountsPayable)
def update_accounts_payable(
    *,
    db: Session = Depends(get_db),
    ap_id: int,
    ap_in: schemas.AccountsPayableCreate,
) -> Any:
    db_account = db.query(models.AccountsPayable).filter(models.AccountsPayable.id_contas_pagar == ap_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Update main data
    update_data = ap_in.dict(exclude={"itens"}, exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_account, field, value)
    
    # Refresh items: drop and recreate
    db.query(models.AccountsPayableItem).filter(models.AccountsPayableItem.id_contas_pagar == ap_id).delete()
    
    if ap_in.itens:
        for item in ap_in.itens:
            db_item = models.AccountsPayableItem(
                **item.dict(),
                id_contas_pagar=ap_id
            )
            db.add(db_item)
            
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.delete("/accounts-payable/{ap_id}")
def delete_accounts_payable(
    *,
    db: Session = Depends(get_db),
    ap_id: int,
) -> Any:
    account = db.query(models.AccountsPayable).filter(models.AccountsPayable.id_contas_pagar == ap_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.query(models.AccountsPayableItem).filter(models.AccountsPayableItem.id_contas_pagar == ap_id).delete()
    db.delete(account)
    db.commit()
    return {"message": "Account deleted successfully"}
