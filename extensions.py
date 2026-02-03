import mysql.connector
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# ---------- DATABASE ----------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="girish",
        password="Girish*40111237",
        database="trauma_ai"
    )

# ---------- AUTH ----------
login_manager = LoginManager()
login_manager.login_view = "auth.login"

# ---------- CSRF ----------
csrf = CSRFProtect()
