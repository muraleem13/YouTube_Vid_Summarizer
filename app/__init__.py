import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    from app.controllers.main_controller import bp as main_bp
    app.register_blueprint(main_bp)

    return app
