# Architecture Documentation - GBlack Store

## System Overview
GBlack Store is a full-stack e-commerce application built with Django (Backend) and React (Frontend). It features a complete purchase flow, inventory management, and guest checkout capabilities.

## Tech Stack
-   **Backend**: Python, Django, Django REST Framework (DRF)
-   **Frontend**: JavaScript, React, TailwindCSS, Axios
-   **Database**: SQLite (Development), PostgreSQL (Production ready)
-   **Containerization**: Docker (Frontend)

## Key Components

### Backend (`loja` App)
The core logic resides in the `loja` Django app.

#### Models
-   **`Produto`**: Represents products with inventory (`estoque`), price, and type.
-   **`Carrinho` & `CartItem`**: Manages user shopping carts. Supports both authenticated users (`Cliente`) and guests (`session_id`).
-   **`Venda` & `ItemVenda`**: Represents completed orders and their items.
-   **`PaymentTransaction`**: Records payment attempts and statuses.
-   **`StoreConfig`**: Singleton configuration for store settings (e.g., cart expiration).

#### API (`api_views.py`)
-   **`ProdutoViewSet`**: CRUD for products. Includes `related` action for cross-selling.
-   **`CarrinhoViewSet`**: Manages cart operations.
    -   **Stock Reservation**: Decrements stock immediately on `add_item`.
    -   **Guest Support**: Uses `X-Guest-ID` header to identify guest carts.
-   **`VendaViewSet`**: Handles order processing.
    -   **`checkout` action**: Atomic transaction to validate stock, create order, and record payment.

#### Background Jobs
-   **`cleanup_carts`**: Management command to release stock from expired carts (inactive > X days).

### Frontend (`frontend`)
A Single Page Application (SPA) built with React.

#### Key Pages
-   **`Home`**: Product listing.
-   **`ProductDetail`**: Product details and "Add to Cart".
-   **`Cart`**: Cart management, quantity updates, and related products.
-   **`Checkout`**: Address selection and payment confirmation.

#### API Integration (`api.js`)
-   **Axios Interceptor**: Automatically attaches `Authorization` token (if logged in) or `X-Guest-ID` (if guest) to every request.

## Data Flow
1.  **User Interaction**: User interacts with React frontend.
2.  **API Request**: Frontend sends JSON request to Django API.
3.  **Processing**: Django ViewSet processes request, interacts with Models/DB.
4.  **Response**: JSON response returned to Frontend.

## Deployment & Verification
-   **Pre-Deploy Script**: `scripts/pre_deploy.py` runs backend tests and builds frontend to ensure stability.
