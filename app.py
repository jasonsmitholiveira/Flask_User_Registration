import os
import secrets
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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI') or 'postgresql://user:password@localhost/database'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') or 'smtp.example.com'
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'your_email@example.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or 'your_email_password'

mail = Mail(app)

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)

class CadastroForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=12)])
    confirmar_senha = PasswordField('Confirmar Senha', [
        validators.DataRequired(),
        validators.EqualTo('senha', message='Senhas devem ser iguais')
    ])

def send_verification_email(user):
    # Generate the verification token using the function you've defined
    token = generate_verification_token(user)

    # Create an email message
    subject = "Confirme seu endereço de e-mail"
    recipients = [user.email]
    sender = app.config['MAIL_USERNAME']
    message_body = f"Para confirmar seu endereço de e-mail, clique no link a seguir:\n{url_for('confirm_email', token=token, _external=True)}"

    message = Message(subject=subject, recipients=recipients, sender=sender)
    message.body = message_body

    # Send the email
    try:
        mail.send(message)
        flash('Um e-mail de verificação foi enviado para seu endereço de e-mail. Verifique sua caixa de entrada.', 'info')
    except Exception as e:
        flash('Erro ao enviar o e-mail de verificação. Por favor, tente novamente mais tarde.', 'error')

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
            hashed_password = generate_password_hash(senha, method='pbkdf2:sha256', salt_length=16)
            novo_usuario = User(email=email, senha_hash=hashed_password)
            db.session.add(novo_usuario)
            db.session.commit()

            send_verification_email(novo_usuario)

            flash('Cadastro realizado com sucesso. Verifique seu e-mail para ativar sua conta.', 'success')

    return render_template('cadastro2.html', form=form)

@app.route('/login')
def login():
    return redirect(url_for('index'))  # Redirect to your login page

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter_by(email=email).first()
        if user:
            user.email_confirmed = True
            db.session.commit()
            flash('Seu e-mail foi confirmado com sucesso!', 'success')
        else:
            flash('Token de confirmação inválido', 'error')
    except Exception as e:
        flash('Erro ao confirmar o e-mail', 'error')
    return redirect(url_for('index'))

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='reset-password', max_age=3600)
        user = User.query.filter_by(email=email).first()
        if user:
            if request.method == 'POST':
                new_password = request.form['new_password']
                user.senha_hash = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=16)
                db.session.commit()
                flash('Senha redefinida com sucesso!', 'success')
                return redirect(url_for('login'))
        else:
            flash('Token de redefinição de senha inválido', 'error')
    except Exception as e:
        flash('Erro ao redefinir a senha', 'error')
    return render_template('reset_password.html', token=token)

def generate_verification_token(user):
    return serializer.dumps(user.email, salt='email-confirm')

def generate_password_reset_token(user):
    return serializer.dumps(user.email, salt='reset-password')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.config['DEBUG'] = True
    app.run(port=8000)
