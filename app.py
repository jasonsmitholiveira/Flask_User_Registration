import os
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configura a URL do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seu_banco_de_dados.db'
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Defina sua chave secreta aqui
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Define o modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)

# Define o formulário de cadastro
class CadastroForm(FlaskForm):
    email = StringField('E-mail', validators=[validators.InputRequired(), validators.Email()])
    senha = PasswordField('Senha', validators=[validators.InputRequired(), validators.EqualTo('confirmar_senha', message='As senhas devem ser iguais.')])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[validators.InputRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise validators.ValidationError('E-mail já cadastrado.')

# Verifica as extensões de arquivo permitidas
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota para o cadastro de usuário
@app.route('/', methods=['GET', 'POST'])
def cadastro_usuario():
    form = CadastroForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Gere o hash da senha antes de armazená-la
        hashed_password = generate_password_hash(form.senha.data)

        novo_usuario = User(
            email=form.email.data,
            senha=hashed_password,
        )

        existing_user_by_email = User.query.filter_by(email=form.email.data).first()

        if existing_user_by_email:
            flash('E-mail já cadastrado', 'error')
        else:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso', 'success')

    return render_template('cadastro2.html', form=form)

# Rota para login (você pode adicionar a funcionalidade de login aqui)
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.config['DEBUG'] = True
    app.run(port=8000)
