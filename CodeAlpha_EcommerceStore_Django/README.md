# CodeAlpha Task 1 — E-commerce Store

A beginner-friendly demo e-commerce app built with Python Django, HTML, CSS, JavaScript, and SQLite.

## Features
- Product listing and product details
- Session-based shopping cart with quantity updates
- User registration and login using Django authentication
- Demo checkout and order history
- Product stock updates
- Django admin for products and orders
- Responsive layout

## Windows + VS Code setup
1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Extract this ZIP file.
3. Open the extracted `CodeAlpha_EcommerceStore_Django` folder in VS Code.
4. Open **Terminal → New Terminal**.
5. Run these commands one at a time:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py makemigrations shop
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_products
.\.venv\Scripts\python.exe manage.py runserver
```

6. Open http://127.0.0.1:8000/ in your browser.
7. Register an account, add products to cart, and place a demo order.

## Optional admin
Create an admin account:
```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```
Then visit http://127.0.0.1:8000/admin/.

## Database
Uses SQLite by default, so no MongoDB/MySQL setup is required. Django creates `db.sqlite3` after migrations.

## Important
This is an educational demo. Checkout records orders but does **not** collect payments. Do not deploy with the development secret key or DEBUG enabled.
