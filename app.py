from flask import Flask, render_template
from config import Config
from extensions import login_manager, csrf

from modules.auth.routes import auth_bp
from modules.chat.routes import chat_bp
from modules.history.routes import history_bp
from modules.profile.routes import profile_bp
from modules.admin.routes import admin_bp
from modules.trauma.analyzer import trauma_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(trauma_bp)

    @app.route("/")
    def landing():
        return render_template("landing.html")

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
