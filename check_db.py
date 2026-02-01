import sys
import os
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.models.product import Product

db = SessionLocal()
products = db.query(Product).all()
print(f"Total products: {len(products)}")
for p in products:
    print(f"ID: {p.id_produto}, Nome: {p.nome}")
db.close()
