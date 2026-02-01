# 🚀 Guia de Início Rápido - Meu Caixa Frontend

## 📋 Pré-requisitos

- Python 3.8+
- FastAPI instalado
- Banco de dados configurado (SQLite ou PostgreSQL)

## 🏃 Como Executar

### 1. Ativar o Ambiente Virtual (se necessário)

```powershell
# Se estiver usando venv no Windows
.\Scripts\activate
```

### 2. Instalar Dependências

```powershell
pip install -r requirements.txt
```

### 3. Iniciar o Servidor

```powershell
# A partir do diretório raiz do projeto
uvicorn app.main:app --reload
```

### 4. Acessar a Aplicação

Abra seu navegador e acesse:
```
http://localhost:8000
```

Você será automaticamente redirecionado para a tela de login.

## 🔑 Credenciais de Teste

Para testar a aplicação, você precisará criar um usuário primeiro. Você pode fazer isso de duas formas:

### Opção 1: Via API Docs (Swagger)

1. Acesse: `http://localhost:8000/docs`
2. Vá para o endpoint `POST /users/`
3. Clique em "Try it out"
4. Insira os dados do usuário:
```json
{
  "nome": "Admin",
  "email": "admin@meucaixa.com",
  "senha": "admin123"
}
```
5. Execute a requisição

### Opção 2: Via Script Python

Crie um arquivo `create_user.py` na raiz do projeto:

```python
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

user = User(
    nome="Admin",
    email="admin@meucaixa.com",
    senha=get_password_hash("admin123")
)

db.add(user)
db.commit()
db.close()

print("Usuário criado com sucesso!")
```

Execute:
```powershell
python create_user.py
```

## 🎯 Testando as Funcionalidades

### 1. Login
- Email: `admin@meucaixa.com`
- Senha: `admin123`

### 2. Dashboard (Contas a Receber)
Após o login, você será direcionado automaticamente para a tela de **Contas a Receber**.

### 3. Criar Dados de Teste

Para popular o sistema com dados de teste, você pode usar os endpoints da API:

#### Criar Cliente
```bash
POST http://localhost:8000/clients/
{
  "nome": "João Silva",
  "telefone": "(11) 98765-4321",
  "email": "joao@email.com",
  "limite_credito": 1000.00
}
```

#### Criar Categoria
```bash
POST http://localhost:8000/products/categories/
{
  "nome": "Alimentos"
}
```

#### Criar Produto
```bash
POST http://localhost:8000/products/
{
  "nome": "Arroz 5kg",
  "id_categoria": 1,
  "preco_custo": 15.00,
  "preco_venda": 25.00
}
```

#### Criar Venda
```bash
POST http://localhost:8000/sales/
{
  "id_cliente": 1,
  "status_pagamento": "Pendente",
  "forma_pagamento": "Pix",
  "valor_total": 100.00,
  "itens": [
    {
      "id_produto": 1,
      "qtde": 4,
      "valor_unitario": 25.00
    }
  ]
}
```

## 🎨 Funcionalidades Implementadas

### ✅ Completas
- [x] Tela de Login com autenticação JWT
- [x] Dashboard de Contas a Receber
- [x] Cards de estatísticas (Total, Pago, Pendente, Parcial)
- [x] Tabela de vendas com dados dinâmicos
- [x] Navegação entre views
- [x] Dark Mode (toggle no sidebar)
- [x] Design responsivo
- [x] Sidebar com menu hierárquico

## 🐛 Troubleshooting

### Problema: "Module not found"
**Solução:** Certifique-se de que está no diretório correto e que o ambiente virtual está ativado.

### Problema: "CORS error"
**Solução:** Verifique as configurações de CORS em `app/core/config.py`

### Problema: "401 Unauthorized"
**Solução:** 
1. Verifique se o token está sendo salvo no localStorage
2. Limpe o cache do navegador
3. Faça logout e login novamente

### Problema: Tabela vazia no dashboard
**Solução:** 
1. Crie vendas de teste usando a API
2. Verifique se o endpoint `/sales/` está retornando dados
3. Abra o Console do navegador para ver possíveis erros

## 📱 Testando Responsividade

1. Abra o DevTools (F12)
2. Clique no ícone de dispositivo móvel (Ctrl+Shift+M)
3. Teste em diferentes resoluções:
   - Mobile: 375x667 (iPhone SE)
   - Tablet: 768x1024 (iPad)
   - Desktop: 1920x1080

## 🌙 Testando Dark Mode

1. Clique no ícone de lua no sidebar (próximo ao botão de logout)
2. A preferência é salva no localStorage
3. Ao recarregar a página, o tema deve ser mantido

## 📊 Verificando Dados no Banco

### SQLite (padrão)
```powershell
# Instalar sqlite3 (se necessário)
# Abrir o banco
sqlite3 sql_app.db

# Listar tabelas
.tables

# Ver vendas
SELECT * FROM vendas;

# Ver clientes
SELECT * FROM clientes;

# Sair
.exit
```

## 🔧 Configurações Adicionais

### Alterar Porta do Servidor
```powershell
uvicorn app.main:app --reload --port 8080
```

### Modo de Produção (sem reload)
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 Próximos Passos

1. **Testar todas as funcionalidades atuais**
   - Login/Logout
   - Navegação
   - Dark Mode
   - Visualização de vendas

2. **Implementar Nova Venda**
   - Formulário completo
   - Validações
   - Integração com API

3. **Implementar CRUDs**
   - Clientes
   - Produtos
   - Categorias

4. **Adicionar Funcionalidades Avançadas**
   - Filtros
   - Busca
   - Paginação
   - Exportação

## 📞 Suporte

Para mais informações, consulte:
- `app/main.py` - Configuração do servidor
- `app/routers/` - Endpoints da API
- `app/templates/index.html` - Frontend completo

---

**Desenvolvido com ❤️ para Meu Caixa**
**Versão:** 1.0.0
**Data:** 2026-01-18
