from flask import Flask, redirect, url_for, render_template, session
from flask_wtf.csrf import CSRFProtect

from config import Config
from database.database import init_db

from backend.routes.auth_routes import auth_bp
from backend.routes.dashboard_routes import dashboard_bp
from backend.routes.weather_routes import weather_bp
from backend.routes.analysis_routes import analysis_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static"
    )

    # Load application configuration
    app.config.from_object(Config)

    # Enable CSRF protection
    CSRFProtect(app)

    # Initialize database
    init_db(app)

    # Register application routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(analysis_bp)

    # Home route
    @app.get("/")
    def index():
        if session.get("user_id"):
            return redirect(url_for("dashboard.dashboard"))

        return redirect(url_for("auth.login"))

    # 404 error page
    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=app.config["DEBUG"],
        host="127.0.0.1",
        port=5000
    )