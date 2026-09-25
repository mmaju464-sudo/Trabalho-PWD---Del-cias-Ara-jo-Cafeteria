from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)


# ==========================================
# CONFIGURAÇÕES
# ==========================================

app.config["UPLOAD_FOLDER"] = "ifitness/static/uploads"

app.secret_key = "chave_secreta"

app.permanent_session_lifetime = 3600


# ==========================================
# BANCO DE DADOS
# ==========================================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ifitness.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)


# ==========================================
# ROTAS
# ==========================================

from ifitness import rotas