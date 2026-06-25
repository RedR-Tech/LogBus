from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'Gk9!@2xLp3#mZ8$qW1_vY5&tX7*rB4+a'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "uploads")
os.makedirs('uploads', exist_ok=True)

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.aluno import aluno_bp
from routes.cadastro import cadastro_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(cadastro_bp)

if __name__ == '__main__':
    app.run(debug=True)