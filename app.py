from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = '52324f6c083f63119e7b3813693952eed20b07223c6af499aaa872104b9b1c5a'

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