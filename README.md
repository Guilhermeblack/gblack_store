# GBlack Store - E-commerce Django

Sistema de loja online desenvolvido em Django com recursos completos de e-commerce, incluindo carrinho de compras, checkout, gerenciamento de produtos e feed de conteúdo.

## 📋 Estado Atual do Projeto

### ✅ Funcionalidades Implementadas
- Sistema de autenticação de usuários (cadastro e login)
- Catálogo de produtos com imagens (Cloudinary)
- Carrinho de compras funcional
- Fluxo de checkout (carrinho → endereço → pagamento)
- Painel administrativo Django
- Sistema de pedidos e vendas
- Gestão de estoque
- Integração com Cloudinary para imagens

### ⚠️ Problemas Conhecidos
1. **Dependência PWA**: Referências ao `django-pwa` foram comentadas temporariamente
2. **Template base.html**: Erro de sintaxe na seção de produtos (linhas 98-101)
3. **Testes**: 2 de 4 testes unitários passando (50%)

### 🚧 Em Desenvolvimento
- Sistema de Feed para posts e orientações sobre produtos
- Agendamento de posts
- Períodos de desconto programados
- Toggle de disponibilidade de produtos

## 🛠️ Tecnologias Utilizadas

- **Python**: 3.11+
- **Django**: 3.0+
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Cloudinary**: Armazenamento de imagens
- **Bootstrap**: Framework CSS

## 📦 Dependências Principais

```
Django>=3.0
cloudinary
Pillow
```

## 🚀 Instalação e Execução Local

### Pré-requisitos

1. **Python 3.11+**
   ```bash
   python --version
   ```
   Se não tiver instalado: https://www.python.org/downloads/

2. **pip** (gerenciador de pacotes Python)
   ```bash
   pip --version
   ```

### Passo a Passo

#### 1. Clone o Repositório
```bash
git clone https://github.com/guilhermeblack/gblack_store.git
cd gblack_store
```

#### 2. Crie um Ambiente Virtual (Recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

#### 3. Instale as Dependências
```bash
pip install Django cloudinary Pillow
```

#### 4. Configure o Banco de Dados

**IMPORTANTE**: As migrações antigas foram regeneradas. Execute:

```bash
# Remova o banco de dados antigo (se existir)
del db.sqlite3  # Windows
# rm db.sqlite3  # Linux/macOS

# Execute as migrações
python manage.py migrate
```

#### 5. Crie um Superusuário (Admin)
```bash
python manage.py createsuperuser
```
Siga as instruções para criar username, email e senha.

#### 6. Execute o Servidor de Desenvolvimento
```bash
python manage.py runserver
```

O projeto estará disponível em: **http://127.0.0.1:8000/**

#### 7. Acesse o Admin
Painel administrativo: **http://127.0.0.1:8000/admin/**

Use as credenciais do superusuário criado no passo 5.

## 🧪 Executando Testes

### Testes Unitários
```bash
# Todos os testes
python manage.py test

# Testes específicos de vendas
python manage.py test loja.tests_sales

# Com verbosidade
python manage.py test loja.tests_sales -v 2
```

### Resultados Esperados
- ✅ `test_add_to_cart`: Adicionar produto ao carrinho
- ✅ `test_checkout_address_creation`: Criar endereço de entrega
- ⚠️ `test_checkout_cart_view`: Erro de template (conhecido)
- ⚠️ `test_process_payment_and_order_creation`: Em correção

## 📁 Estrutura do Projeto

```
gblack_store/
├── gbstr/              # Configurações do projeto
│   ├── settings.py     # Configurações principais
│   ├── urls.py         # URLs principais
│   └── wsgi.py
├── loja/               # App principal
│   ├── models.py       # Modelos (Cliente, Produto, Carrinho, Venda)
│   ├── views.py        # Views principais
│   ├── checkout_views.py  # Views do checkout
│   ├── forms.py        # Formulários
│   ├── admin.py        # Configuração do admin
│   ├── templates/      # Templates HTML
│   └── static/         # Arquivos estáticos (CSS, JS, imagens)
├── manage.py           # Script de gerenciamento Django
└── README.md
```

## 🗃️ Modelos Principais

### Cliente (User)
- Estende `AbstractUser` do Django
- Campos: username, email, cpf, telefone, first_name, last_name
- Relacionamentos: carrinho, endereços, vendas

### Produto
- Campos: nome, descrição, preço, imagem, tipo, estoque
- Tipos: Relógio (R), Acessório (A), Vestuário (V)

### Carrinho
- Relacionamento OneToOne com Cliente
- Contém múltiplos CartItems

### Venda
- Campos: cliente, endereço, total, status, data
- Status: PENDING, PAID, SHIPPED, DELIVERED, CANCELED
- Relacionamentos: items (ItemVenda), transactions (PaymentTransaction)

## 🔧 Correções Necessárias

### 1. Corrigir Template base.html
**Arquivo**: `loja/templates/blocks/base.html` (linhas 98-101)

**Problema**: Tag `{% ifchanged %}` não fechada corretamente

**Solução**: Fechar tag na mesma linha ou simplificar lógica do menu

### 2. Instalar ou Remover PWA
**Opção A - Instalar**:
```bash
pip install django-pwa
```
Adicionar `'pwa'` em `INSTALLED_APPS` no `settings.py`

**Opção B - Remover** (atual):
Referências já foram comentadas em `base.html`

## 📝 Configuração do Cloudinary

No arquivo `settings.py`, configure suas credenciais:

```python
cloudinary.config(
    cloud_name="seu_cloud_name",
    api_key="sua_api_key",
    api_secret="seu_api_secret"
)
```

## 🌐 URLs Principais

- `/` - Homepage com produtos
- `/conta` - Painel do usuário
- `/checkout/cart/` - Carrinho de compras
- `/checkout/address/` - Endereço de entrega
- `/checkout/payment/` - Pagamento
- `/checkout/success/` - Confirmação de pedido
- `/admin/` - Painel administrativo

## 📞 Suporte

Para problemas ou dúvidas:
- Abra uma issue no GitHub
- Contato: gblacklojaonline@gmail.com

## 📄 Licença

Projeto GBlackTech v2.0

---

**Última atualização**: Dezembro 2025
