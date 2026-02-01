from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import users, auth, clients, products, finance, sales

# Create tables
Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app import models

def ensure_default_client():
    db = SessionLocal()
    try:
        default_client = db.query(models.Client).filter(models.Client.nome == "Consumidor Final").first()
        if not default_client:
            default_client = models.Client(
                nome="Consumidor Final",
                telefone="0000000000",
                email="consumidor@balcao.com",
                limite_credito=0
            )
            db.add(default_client)
            db.commit()
            print("Default client 'Consumidor Final' created.")
    finally:
        db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/openapi.json"
)

@app.on_event("startup")
def startup_event():
    ensure_default_client()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth.router, prefix=f"/login", tags=["login"])
app.include_router(users.router, prefix=f"/users", tags=["users"])
app.include_router(clients.router, prefix=f"/clients", tags=["clients"])
app.include_router(products.router, prefix=f"/products", tags=["products"])
app.include_router(finance.router, prefix=f"/finance", tags=["finance"])
app.include_router(sales.router, prefix=f"/sales", tags=["sales"])


# Serve arquivos estáticos da pasta `templates` em /templates
app.mount("/templates", StaticFiles(directory="app/templates", html=True), name="templates")


# Se alguém acessar / redireciona para a tela de login
@app.get("/", include_in_schema=False)
def admin_index():
    return RedirectResponse("/templates/")


# Rota alternativa para abrir o login
@app.get("/templates/login", include_in_schema=False)
def admin_login():
    return FileResponse("app/templates/index.html")