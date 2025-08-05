# Vault Project

A secure password and notes manager built with Django and Django REST Framework.

---

### 1. Clone the repository
```
git clone https://github.com/gitofvn/vault_project
cd vault_project
```



2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # For Linux/Mac users
.venv\Scripts\activate     # For Windows users


3. Install dependencies
pip install -r requirements.txt


4. Set up environment variables and create a .env file in the project root, containing the line below
MASTER_KEY=Kk0y3so-1Y5R1n2M32WBvLFiS-D9h7mW3ubH3EzpAQI=

Note: This key is for testing and local use only!


5. Run migrations
python manage.py migrate


6. Create a superuser (optional)
python manage.py createsuperuser


7. Run the development server
python manage.py runserver


8. Open your browser at http://127.0.0.1:8000
