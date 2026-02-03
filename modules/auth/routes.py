from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, UserMixin
from extensions import get_db
from extensions import login_manager

auth_bp = Blueprint("auth", __name__)

class User(UserMixin):
    def __init__(self, id, name, email, password, created_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at  # Placeholder, can be set if needed

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    u = cur.fetchone()
    cur.close()
    db.close()
    if u:
        return User(*u)
    return None

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cur.fetchone():
            flash("Email already exists")
            return redirect("/register")

        cur.execute(
            "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
            (name,email,password)
        )
        db.commit()
        cur.close()
        db.close()

        flash("Registration successful")
        return redirect("/login")

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        u = cur.fetchone()
        cur.close()
        db.close()

        if u and check_password_hash(u[3], password):
            login_user(User(*u))
            return redirect("/dashboard")

        flash("Invalid credentials")

    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
