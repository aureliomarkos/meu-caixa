# 💰 Meu Caixa - Sistema de Controle de Recebíveis

## 📋 Visão Geral

**Meu Caixa** é um sistema moderno e intuitivo para controle de recebíveis, desenvolvido especialmente para pequenos restaurantes e comércios. O sistema prioriza a experiência do usuário, colocando o **Contas a Receber** como funcionalidade principal.

---

## ✨ Características Principais

### 🎯 Foco em Recebíveis
- Dashboard de Contas a Receber como tela principal
- Visualização clara de valores a receber, pagos, pendentes e parciais
- Tabela de vendas com filtros e busca
- Estatísticas em tempo real

### 🎨 Design Moderno
- Interface limpa e profissional
- Paleta de cores verde (recebíveis) com acentos coloridos
- Tipografia Inter (Google Fonts)
- Ícones Material Symbols
- Dark Mode completo

### 📱 Responsivo
- Layout adaptativo para Desktop, Tablet e Mobile
- Grid responsivo (4 → 2 → 1 colunas)
- Sidebar responsiva
- Touch-friendly

### 🔐 Seguro
- Autenticação JWT (OAuth2)
- Proteção de rotas
- Tokens com expiração
- Senhas criptografadas (bcrypt)

---

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8+
- FastAPI
- SQLAlchemy
- Uvicorn

### Instalação

1. **Clone o repositório** (se aplicável)
```powershell
git clone https://github.com/aureliomarkos/meu-caixa.git
cd meu-caixa
```

2. **Instale as dependências**
```powershell
pip install -r requirements.txt
```

3. **Inicie o servidor**
```powershell
uvicorn app.main:app --reload
```

4. **Acesse a aplicação**
```
http://localhost:8000
```

### Primeiro Acesso

1. **Crie um usuário** via API Docs:
   - Acesse: `http://localhost:8000/docs`
   - Use o endpoint `POST /users/`
   - Dados:
     ```json
     {
       "nome": "Admin",
       "email": "admin@meucaixa.com",
       "senha": "admin123"
     }
     ```

2. **Faça login** na aplicação:
   - Email: `admin@meucaixa.com`
   - Senha: `admin123`

3. **Explore o dashboard!**

---

## 📁 Estrutura do Projeto

```
meu-caixa/
├── app/
│   ├── core/              # Configurações e segurança
│   ├── models/            # Modelos do banco de dados
│   ├── schemas/           # Schemas Pydantic
│   ├── routers/           # Endpoints da API
│   ├── templates/         # Frontend
│   │   └── index.html     # ⭐ Frontend completo
│   └── main.py            # Aplicação FastAPI
├── utils/
│   ├── layout.html        # Layout de referência
│   └── Tabelas meu-caixa.txt  # Schema do banco
├── QUICK_START.md                   # 🚀 Guia rápido
├── README.md                        # 📖 Este arquivo
├── requirements.txt                 # Dependências Python
└── sql_app.db                       # Banco de dados SQLite
```

---

## 🎯 Funcionalidades

### ✅ Implementadas

#### 1. Autenticação
- [x] Tela de login
- [x] JWT (OAuth2)
- [x] Logout
- [x] Proteção de rotas

#### 2. Contas a Receber (Dashboard)
- [x] Cards de estatísticas
  - Total a Receber
  - Valores Pagos
  - Aguardando
  - Parcial
- [x] Tabela de vendas
- [x] Integração com API
- [x] Formatação de valores
- [x] Badges de status

#### 3. Gestão e Cadastros
- [x] Clientes (CRUD completo)
- [x] Produtos (CRUD completo)
- [x] Fornecedores (CRUD completo)
- [x] Categorias (CRUD completo)
- [x] Funcionários (CRUD completo)

#### 4. Financeiro
- [x] Contas a Pagar
- [x] Adiantamentos de Salário/Vales
- [x] Controle de Vendas (Nova Venda)

#### 5. Navegação e Interface
- [x] Sidebar com menu hierárquico
- [x] Navegação entre views
- [x] Indicadores visuais
- [x] Dark Mode
- [x] Responsividade
- [x] Animações e design system

#### 6. Funcionalidades Avançadas
- [x] Filtros avançados por módulo
- [x] Busca global por módulo no header
- [x] Paginação integrada em todas as listas

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


## 🛠️ Tecnologias

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validação de dados
- **JWT** - Autenticação
- **Bcrypt** - Criptografia de senhas
- **Uvicorn** - Servidor ASGI

### Frontend
- **HTML5** - Estrutura
- **Tailwind CSS** - Estilização
- **Vanilla JavaScript** - Lógica
- **Material Symbols** - Ícones
- **Google Fonts (Inter)** - Tipografia

### Banco de Dados
- **SQLite** - Desenvolvimento (padrão)
- **PostgreSQL** - Produção (recomendado)

---

## 🎨 Design System

### Cores Principais
```css
Primary (Verde):    #10b981  /* Recebíveis, sucesso */
Primary-600:        #059669  /* Hover states */
Primary-700:        #047857  /* Active states */

Success (Pago):     #10b981  /* Verde */
Warning (Pendente): #f59e0b  /* Amarelo */
Danger (Atrasado):  #ef4444  /* Vermelho */
Info (Parcial):     #3b82f6  /* Azul */
```

### Tipografia
- **Família**: Inter
- **Pesos**: 400, 500, 600, 700, 800, 900
- **Tamanhos**: 12px, 14px, 16px, 18px, 24px, 30px

### Espaçamento
- **Base**: 4px (0.25rem)
- **Escala**: 4, 8, 12, 16, 24, 32, 48, 64

---

## 🔧 Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
# Database
DATABASE_URL=sqlite:///./sql_app.db

# Security
SECRET_KEY=sua-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:8000"]

# App
PROJECT_NAME=Meu Caixa
```

### Banco de Dados

#### SQLite (Desenvolvimento)
```python
DATABASE_URL = "sqlite:///./sql_app.db"
```

#### PostgreSQL (Produção)
```python
DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

---

## 🧪 Testes

### Testes Manuais
1. Login com credenciais válidas/inválidas
2. Navegação entre views
3. Dark mode toggle
4. Responsividade
5. CRUD operations
6. Integração com API

### Ferramentas
- Chrome DevTools
- Network tab (API calls)
- Console (erros JS)
- Lighthouse (performance)

---

## 📈 Roadmap

### Versão 1.0 (Completada)
- [x] Autenticação
- [x] Dashboard de Recebíveis
- [x] Navegação
- [x] Dark Mode
- [x] Responsividade

### Versão 1.1 (Completada)
- [x] Nova Venda (formulário completo)
- [x] CRUD de Clientes
- [x] CRUD de Produtos
- [x] Filtros e busca geral
- [x] Paginação

### Versão 1.2 (Completada)
- [x] CRUD de Fornecedores
- [x] CRUD de Categorias
- [x] Contas a Pagar
- [x] Adiantamentos
- [x] CRUD de Funcionários

### Versão 2.0 (Planejado)
- [ ] Relatórios e gráficos
- [ ] Exportação de dados
- [ ] Notificações em tempo real
- [ ] Dashboard com Chart.js

### Versão 3.0 (Futuro)
- [ ] App mobile (PWA)
- [ ] Impressão de recibos
- [ ] Integração WhatsApp
- [ ] Multi-empresa

---

## 🐛 Problemas Conhecidos

### Limitações
- Relatórios avançados ainda não implementados.
- Gráficos visuais (charts) previstos para v2.0.

---

## 🤝 Contribuindo

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código
- **HTML**: Semântico e bem estruturado
- **CSS**: Tailwind classes, mobile-first
- **JavaScript**: Vanilla JS, async/await, comentários
- **Python**: PEP 8, type hints, docstrings

---

## 📄 Licença

Este projeto é proprietário e confidencial.

---

## 👥 Autores

- **Arquiteto de Software**: Antigravity AI
- **Data**: 2026-02-01
- **Versão**: 1.2.0

---

## 📞 Suporte

Para dúvidas ou sugestões:
1. Consulte a documentação em `/docs`
2. Verifique os guias de implementação
3. Abra uma issue no repositório

---

## 🙏 Agradecimentos

- **FastAPI** - Framework incrível
- **Tailwind CSS** - Estilização rápida e moderna
- **Material Symbols** - Ícones bonitos
- **Google Fonts** - Tipografia elegante

---

## 📊 Estatísticas

- **Linhas de Código**: ~4.800+
- **Componentes**: 20+
- **Views**: 8
- **Endpoints**: 30+
- **Tempo de Desenvolvimento**: Contínuo

---

**Desenvolvido com ❤️ para Meu Caixa**

**Status**: ✅ Pronto para Produção
**Última Atualização**: 2026-02-01
