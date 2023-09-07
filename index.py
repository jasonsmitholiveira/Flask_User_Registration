from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seu_banco_de_dados.db'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['AUTH0_CLIENT_ID'] = ''
app.config['AUTH0_CLIENT_SECRET'] = ''
app.config['AUTH0_DOMAIN'] = ''
app.config['DEBUG'] = True  # Set DEBUG mode explicitly

db = SQLAlchemy(app)
migrate = Migrate(app, db)
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=app.config['AUTH0_CLIENT_ID'],
    client_secret=app.config['AUTH0_CLIENT_SECRET'],
    authorize_url='https://{}/authorize'.format(app.config['AUTH0_DOMAIN']),
    authorize_params=None,
    authorize_kwargs=None,
    access_token_url='https://{}/oauth/token'.format(app.config['AUTH0_DOMAIN']),
    access_token_params=None,
    access_token_kwargs=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:8000/callback',
    client_kwargs={'scope': 'openid profile email'},
)

class CadastroForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', [
        validators.DataRequired(),
        validators.EqualTo('senha', message='Senhas devem ser iguais')
    ])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def cadastro_usuario():
    form = CadastroForm()

    if request.method == 'POST' and form.validate_on_submit():
        existing_user_by_email = User.query.filter_by(email=form.email.data).first()
        if existing_user_by_email:
            flash('E-mail já cadastrado', 'error')
        else:
            hashed_password = generate_password_hash(form.senha.data)
            novo_usuario = User(email=form.email.data, senha=hashed_password)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso', 'success')

    return render_template('cadastro2.html', form=form)

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('callback', _external=True))

@app.route('/callback')
def callback():
    auth0.authorize_access_token()
    response = auth0.get('userinfo')
    userinfo = response.json()

    # You can use userinfo to manage the user session, store user data, and more.

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()  # Clear the user session
    params = {
        'returnTo': url_for('index', _external=True),
        'client_id': app.config['AUTH0_CLIENT_ID'],
    }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000)
