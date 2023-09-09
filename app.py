from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Substitua pela sua chave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configurações do e-mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Configure o servidor SMTP de envio de e-mails
app.config['MAIL_PORT'] = 587  # Porta SMTP (587 é uma porta comum para TLS)
app.config['MAIL_USE_TLS'] = True  # Usar TLS para criptografia
app.config['MAIL_USERNAME'] = 'jasonsmitholiveira@gmail.com'  # Seu endereço de e-mail
app.config['MAIL_PASSWORD'] = 'dinheiro2020$'  # Sua senha de e-mail

mail = Mail(app)

# Configuração do serializer para gerar tokens seguros
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)



class CadastroForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', [
        validators.DataRequired(),
        validators.EqualTo('senha', message='Senhas devem ser iguais')
    ])

@app.route('/', methods=['GET', 'POST'])
def cadastro_usuario():
    form = CadastroForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        existing_user_by_email = User.query.filter_by(email=email).first()

        if existing_user_by_email:
            flash('E-mail já cadastrado', 'error')
        else:
            hashed_password = generate_password_hash(senha)
            novo_usuario = User(email=email, senha_hash=hashed_password)
            db.session.add(novo_usuario)
            db.session.commit()
            
            # Envie o e-mail de verificação
            send_verification_email(novo_usuario)
            
            flash('Cadastro realizado com sucesso. Verifique seu e-mail para ativar sua conta.', 'success')

    return render_template('cadastro2.html', form=form)

@app.route('/login')
def login():
    return redirect('http://localhost:8000/')  # Redirect to your login page

@app.route('/logout')
def logout():
    session.clear()  # Clear the user session
    return redirect(url_for('index'))  # Redirect to the index page

from itsdangerous import URLSafeTimedSerializer

# Configure o serializer para gerar tokens seguros
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Rota para confirmar o e-mail
@app.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)  # Verifique se o token é válido por 1 hora
        user = User.query.filter_by(email=email).first()
        if user:
            user.email_confirmed = True
            db.session.commit()
            flash('Seu e-mail foi confirmado com sucesso!', 'success')
        else:
            flash('Token de confirmação inválido', 'error')
    except Exception as e:
        flash('Erro ao confirmar o e-mail', 'error')
    return redirect(url_for('index'))  # Redirecionar para a página inicial

# Rota para redefinir a senha
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='reset-password', max_age=3600)  # Verifique se o token é válido por 1 hora
        user = User.query.filter_by(email=email).first()
        if user:
            if request.method == 'POST':
                new_password = request.form['new_password']
                user.senha = generate_password_hash(new_password)
                db.session.commit()
                flash('Senha redefinida com sucesso!', 'success')
                return redirect(url_for('login'))
        else:
            flash('Token de redefinição de senha inválido', 'error')
    except Exception as e:
        flash('Erro ao redefinir a senha', 'error')
    return render_template('reset_password.html', token=token)  # Renderize um formulário para redefinir a senha

# Implemente a função para gerar tokens de verificação e redefinição de senha
def generate_verification_token(user):
    return serializer.dumps(user.email, salt='email-confirm')

def generate_password_reset_token(user):
    return serializer.dumps(user.email, salt='reset-password')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.config['DEBUG'] = True
    app.run(port=8000)


