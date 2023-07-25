from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration for the upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# Função para criar as tabelas do banco de dados
def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    # Importando os módulos de rotas após a definição dos blueprints para evitar a importação circular
    from routes import auth_bp, main_bp

    # Registrando os blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Criando as tabelas do banco de dados antes de executar a aplicação
    create_tables()
    app.run(debug=True)