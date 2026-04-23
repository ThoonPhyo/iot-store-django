# --- IoT Store Project: Setup & Run Commands ---

# [Option 1] Using Pipenv
# -----------------------
pip install pipenv
pipenv install
pipenv shell


# [Option 2] Using standard venv (Manual Setup)
# -----------------------
# 1. Create Virtual Environment
python -m venv venv

# 2. Activate Virtual Environment (Windows)
# ** This is the part to ensure library access **
.\venv\Scripts\activate

# 3. Install Requirements
pip install -r requirements.txt


# [Database & Server]
# -----------------------
# 4. Database Setup
python manage.py makemigrations
python manage.py migrate

# 5. Create Admin (Optional)
python manage.py createsuperuser

# 6. Run Server
python manage.py runserver

# URL: http://127.0.0.1:8000/
