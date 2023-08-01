import os
from flask import Flask, render_template, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, FileField, PasswordField, validators
from werkzeug.security import generate_password_hash
from wtforms import BooleanField
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)  # Generate a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'uploads'  # Add the folder to store uploaded files
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf_cnpj = db.Column(db.String(20), nullable=False, unique=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(10))
    estado_civil = db.Column(db.String(20))
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    endereco_cep = db.Column(db.String(10))
    endereco_logradouro = db.Column(db.String(100))
    endereco_numero = db.Column(db.String(10))
    endereco_complemento = db.Column(db.String(50))
    endereco_bairro = db.Column(db.String(50))
    endereco_cidade = db.Column(db.String(50))
    endereco_estado = db.Column(db.String(50))
    identificacao_arquivo = db.Column(db.String(100))


class CadastroForm(FlaskForm):
    cpf_cnpj = StringField('CPF/CNPJ', validators=[validators.InputRequired()])
    nome_completo = StringField('Nome Completo', validators=[validators.InputRequired()])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[validators.InputRequired()])
    genero = SelectField('Gênero', choices=[('', ''), ('masculino', 'Masculino'), ('feminino', 'Feminino')])
    estado_civil = SelectField('Estado Civil', choices=[('', ''), ('solteiro', 'Solteiro'), ('casado', 'Casado')])
    email = StringField('E-mail', validators=[validators.InputRequired(), validators.Email()])
    telefone = StringField('Telefone', validators=[validators.InputRequired()])
    senha = PasswordField('Senha', validators=[validators.InputRequired(), validators.EqualTo('confirmar_senha', 'As senhas devem ser iguais.')])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[validators.InputRequired()])
    endereco_cep = StringField('CEP', validators=[validators.InputRequired()])
    endereco_logradouro = StringField('Logradouro', validators=[validators.InputRequired()])
    endereco_numero = StringField('Número', validators=[validators.InputRequired()])
    endereco_complemento = StringField('Complemento', validators=[validators.InputRequired()])
    endereco_bairro = StringField('Bairro', validators=[validators.InputRequired()])
    endereco_cidade = StringField('Cidade', validators=[validators.InputRequired()])
    endereco_estado = StringField('Estado', validators=[validators.InputRequired()])
    identificacao = FileField('Identificação', validators=[validators.InputRequired()])
    politica = BooleanField('Aceito os termos e condições ao realizar o cadastro.',
                            validators=[validators.InputRequired()])

    def fetch_address_data(cep):
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)
        data = response.json()
        return data

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise validators.ValidationError('E-mail já cadastrado.')
        pass


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def cadastro_usuario():
    form = CadastroForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Hash the password before storing it
        hashed_password = generate_password_hash(form.senha.data)

        novo_usuario = User(
            cpf_cnpj=form.cpf_cnpj.data,
            nome_completo=form.nome_completo.data,
            data_nascimento=form.data_nascimento.data,
            genero=form.genero.data,
            estado_civil=form.estado_civil.data,
            email=form.email.data,
            telefone=form.telefone.data,
            senha=hashed_password,
            endereco_cep=form.endereco_cep.data,
            endereco_logradouro=form.endereco_logradouro.data,
            endereco_numero=form.endereco_numero.data,
            endereco_complemento=form.endereco_complemento.data,
            endereco_bairro=form.endereco_bairro.data,
            endereco_cidade=form.endereco_cidade.data,
            endereco_estado=form.endereco_estado.data,
        )

        # Handle the uploaded file
        if form.identificacao.data and allowed_file(form.identificacao.data.filename):
            filename = secure_filename(form.identificacao.data.filename)
            form.identificacao.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            novo_usuario.identificacao_arquivo = filename

        # Check if the CPF/CNPJ and email are already registered
        existing_user_by_cpf = User.query.filter_by(cpf_cnpj=form.cpf_cnpj.data).first()
        existing_user_by_email = User.query.filter_by(email=form.email.data).first()

        if existing_user_by_cpf:
            flash('CPF/CNPJ já cadastrado', 'error')
        elif existing_user_by_email:
            flash('E-mail já cadastrado', 'error')
        else:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso', 'success')

    return render_template('cadastro.html', form=form)

@app.route('/verificar_email', methods=['POST'])
def verificar_email():
    email = request.form['email']
    user_exists = User.query.filter_by(email=email).first()

    if user_exists:
        return jsonify({'email_em_uso': True})
    else:
        return jsonify({'email_em_uso': False})


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
