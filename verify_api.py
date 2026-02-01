import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api/v1"

def print_step(msg):
    print(f"\n[STEP] {msg}")

def make_request(method, endpoint, data=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    if data:
        if endpoint == "/login/access-token":
            # Form data for login
            encoded_data = urllib.parse.urlencode(data).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            # JSON for others
            encoded_data = json.dumps(data).encode("utf-8")
    else:
        encoded_data = None

    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            response_body = response.read().decode("utf-8")
            try:
                json_body = json.loads(response_body)
            except:
                json_body = response_body
            return status, json_body, None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return e.code, error_body, e
    except Exception as e:
        return 0, str(e), e

def verify():
    # 1. Create User
    print_step("Creating User")
    user_data = {
        "email": "test@example.com",
        "nome": "Test User",
        "senha": "password123"
    }
    status, body, err = make_request("POST", "/users/", user_data)
    if status == 200:
        print("User created successfully")
    elif status == 400 and "already exists" in str(body):
        print("User already exists")
    else:
        print(f"Failed to create user: {status} {body}")
        sys.exit(1)

    # 2. Login
    print_step("Logging in")
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    status, body, err = make_request("POST", "/login/access-token", login_data)
    if status != 200:
        print(f"Login failed: {status} {body}")
        sys.exit(1)
    
    token = body["access_token"]
    print("Logged in successfully")

    # 3. Create Client
    print_step("Creating Client")
    client_data = {
        "nome": "Test Client",
        "telefone": "123456789",
        "email": "client@example.com",
        "limite_credito": 1000.00
    }
    status, body, err = make_request("POST", "/clients/", client_data, token)
    if status != 200:
        print(f"Failed to create client: {status} {body}")
        sys.exit(1)
    client_id = body["id_cliente"]
    print(f"Client created with ID: {client_id}")

    # 4. Create Category
    print_step("Creating Category")
    category_data = {
        "nome": "Beverages"
    }
    status, body, err = make_request("POST", "/products/categories/", category_data, token)
    if status != 200:
        print(f"Failed to create category: {status} {body}")
        sys.exit(1)
    category_id = body["id_categoria"]
    print(f"Category created with ID: {category_id}")

    # 5. Create Product
    print_step("Creating Product")
    product_data = {
        "nome": "Soda",
        "id_categoria": category_id,
        "preco_custo": 2.50,
        "preco_venda": 5.00
    }
    status, body, err = make_request("POST", "/products/", product_data, token)
    if status != 200:
        print(f"Failed to create product: {status} {body}")
        sys.exit(1)
    product_id = body["id_produto"]
    print(f"Product created with ID: {product_id}")

    # 6. Create Sale
    print_step("Creating Sale")
    sale_data = {
        "id_cliente": client_id,
        "status_pagamento": "Pendente",
        "forma_pagamento": "Dinheiro",
        "valor_total": 10.00,
        "itens": [
            {
                "id_produto": product_id,
                "qtde": 2,
                "valor_unitario": 5.00
            }
        ]
    }
    status, body, err = make_request("POST", "/sales/", sale_data, token)
    if status != 200:
        print(f"Failed to create sale: {status} {body}")
        sys.exit(1)
    sale_id = body["id_vendas"]
    print(f"Sale created with ID: {sale_id}")

    print("\n[SUCCESS] Verification completed successfully!")

if __name__ == "__main__":
    verify()
