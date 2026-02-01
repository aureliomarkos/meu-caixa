from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.database import get_db

router = APIRouter()

# Categories
@router.post("/categories/", response_model=schemas.Category)
def create_category(
    *,
    db: Session = Depends(get_db),
    category_in: schemas.CategoryCreate,
) -> Any:
    category = models.Category(nome=category_in.nome)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/categories/", response_model=List[schemas.Category])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories

# Products
@router.post("/", response_model=schemas.Product)
def create_product(
    *,
    db: Session = Depends(get_db),
    product_in: schemas.ProductCreate,
) -> Any:
    print(f"Recebendo novo produto: {product_in.nome}")
    product = models.Product(**product_in.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/", response_model=List[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    product_in: schemas.ProductCreate,
) -> Any:
    print(f"Atualizando produto ID {product_id}: {product_in.nome}")
    product = db.query(models.Product).filter(models.Product.id_produto == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}")
def delete_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
) -> Any:
    product = db.query(models.Product).filter(models.Product.id_produto == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# Categories
@router.put("/categories/{category_id}", response_model=schemas.Category)
def update_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    category_in: schemas.CategoryCreate,
) -> Any:
    category = db.query(models.Category).filter(models.Category.id_categoria == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.nome = category_in.nome
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.delete("/categories/{category_id}")
def delete_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
) -> Any:
    category = db.query(models.Category).filter(models.Category.id_categoria == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
