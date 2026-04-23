# --- IoT Store Project: Setup & Run Commands ---

### 1. Clone the Repository

```bash
git clone [https://github.com/ThoonPhyo/iot-store-django.git](https://github.com/ThoonPhyo/iot-store-django.git)
cd iot-store-django

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



