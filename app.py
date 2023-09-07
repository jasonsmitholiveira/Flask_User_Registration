from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)

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
        # Generate the password hash before storing it
        hashed_password = generate_password_hash(form.senha.data)

        existing_user_by_email = User.query.filter_by(email=form.email.data).first()

        if existing_user_by_email:
            flash('E-mail já cadastrado', 'error')
        else:
            novo_usuario = User(
                email=form.email.data,
                senha=hashed_password,
            )
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso', 'success')

    return render_template('cadastro2.html', form=form)

@app.route('/login')
def login():
    return redirect('http://localhost:8000/')  # Redirect to your login page

@app.route('/logout')
def logout():
    session.clear()  # Clear the user session
    return redirect(url_for('index'))  # Redirect to the index page

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.config['DEBUG'] = True
    app.run(port=8000)
