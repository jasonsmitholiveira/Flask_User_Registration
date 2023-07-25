from app import db


class Peca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)  # Change the size accordingly if needed
    fabricante = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    valor = db.Column(db.Float, nullable=False)


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(200), nullable=False)
    endereco_completo = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    concorda_termos = db.Column(db.Boolean, nullable=False, default=False)  # Default value set to False