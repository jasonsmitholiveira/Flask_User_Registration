import os
from flask import Flask, render_template, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, FileField, PasswordField, validators
from werkzeug.security import generate_password_hash
from wtforms import BooleanField
import requests
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)  # Gerar uma chave secreta aleatória
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Configurar o URI do banco de dados
app.config['UPLOAD_FOLDER'] = 'uploads'  # Adicionar a pasta para armazenar os arquivos enviados
db = SQLAlchemy(app)

migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Classificações de Gênero
GENERO_CHOICES = [('', ''), ('masculino', 'Masculino'), ('feminino', 'Feminino'), ('outro', 'Outro')]

# Classificações de Estado Civil
ESTADO_CIVIL_CHOICES = [('', ''), ('solteiro', 'Solteiro'), ('casado', 'Casado'), ('divorciado', 'Divorciado'), ('viuvo', 'Viúvo')]

UPLOADS_FOLDER = 'uploads'  # Define the UPLOADS_FOLDER variable

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf_cnpj = db.Column(db.String(14), nullable=False, unique=False)  # CPF/CNPJ do usuário (único e obrigatório)
    nome_completo = db.Column(db.String(100), nullable=False)  # Nome completo do usuário (obrigatório)
    data_nascimento = db.Column(db.Date, nullable=False)  # Data de nascimento do usuário (obrigatório)
    genero = db.Column(db.String(10))  # Gênero do usuário
    estado_civil = db.Column(db.String(20))  # Estado civil do usuário
    email = db.Column(db.String(100), nullable=False, unique=True)  # Email do usuário (único e obrigatório)
    telefone = db.Column(db.String(11), nullable=False)  # Número de telefone do usuário (obrigatório)
    senha = db.Column(db.String(100), nullable=False)  # Senha do usuário (obrigatório)
    endereco_cep = db.Column(db.String(10))  # CEP do endereço do usuário
    endereco_logradouro = db.Column(db.String(100))  # Logradouro do endereço do usuário
    endereco_numero = db.Column(db.String(10))  # Número do endereço do usuário
    endereco_complemento = db.Column(db.String(50))  # Complemento do endereço do usuário
    endereco_bairro = db.Column(db.String(50))  # Bairro do endereço do usuário
    endereco_cidade = db.Column(db.String(50))  # Cidade do endereço do usuário
    endereco_estado = db.Column(db.String(50))  # Estado do endereço do usuário
    identificacao_arquivo = db.Column(db.String(100))  # Nome do arquivo de identificação do usuário


class CadastroForm(FlaskForm):
    # Formulário para cadastro do usuário
    cpf_cnpj = StringField('CPF/CNPJ', validators=[
        validators.InputRequired(),
        validators.Length(min=11, max=14, message="CPF/CNPJ deve ter 11 ou 14 números.")
    ])  # Campo para CPF/CNPJ (obrigatório)
    nome_completo = StringField('Nome Completo', validators=[validators.InputRequired()])  # Campo para nome completo (obrigatório)
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[validators.InputRequired()])  # Campo para data de nascimento (obrigatório)
    genero = SelectField('Gênero', choices=GENERO_CHOICES)  # Campo para selecionar gênero
    estado_civil = SelectField('Estado Civil', choices=ESTADO_CIVIL_CHOICES)  # Campo para selecionar estado civil
    email = StringField('E-mail', validators=[validators.InputRequired(), validators.Email()])  # Campo para email (obrigatório e validado como email)
    telefone = StringField('Telefone', validators=[
        validators.InputRequired(),
        validators.Length(min=11, max=11, message="Telefone deve conter 11 números (DDD + número do telefone, juntos).")
    ])  # Campo para número de telefone (obrigatório)
    senha = PasswordField('Senha', validators=[validators.InputRequired(), validators.EqualTo('confirmar_senha', 'As senhas devem ser iguais.')])  # Campo para senha (obrigatório) e validação de confirmação de senha
    confirmar_senha = PasswordField('Confirmar Senha', validators=[validators.InputRequired()])  # Campo para confirmar senha (obrigatório)
    endereco_cep = StringField('CEP', validators=[validators.InputRequired()])  # Campo para CEP (obrigatório)
    endereco_logradouro = StringField('Logradouro', validators=[validators.InputRequired()])  # Campo para logradouro (obrigatório)
    endereco_numero = StringField('Número', validators=[validators.InputRequired()])  # Campo para número do endereço (obrigatório)
    endereco_complemento = StringField('Complemento', validators=[validators.InputRequired()])  # Campo para complemento do endereço (obrigatório)
    endereco_bairro = StringField('Bairro', validators=[validators.InputRequired()])  # Campo para bairro do endereço (obrigatório)
    endereco_cidade = StringField('Cidade', validators=[validators.InputRequired()])  # Campo para cidade do endereço (obrigatório)
    endereco_estado = StringField('Estado', validators=[validators.InputRequired()])  # Campo para estado do endereço (obrigatório)
    identificacao = FileField('Identificação', validators=[validators.InputRequired()], render_kw={"multiple": True})  # Allow multiple file uploads
    politica = BooleanField('Aceito os termos e condições ao realizar o cadastro.', validators=[validators.InputRequired()])  # Campo para aceitar os termos e condições ao realizar o cadastro (obrigatório)

    def fetch_address_data(cep):
        # Função para buscar dados de endereço com base no CEP
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)
        data = response.json()
        return data

    def validate_email(self, field):
        # Função para validar se o email já está cadastrado no banco de dados
        if User.query.filter_by(email=field.data).first():
            raise validators.ValidationError('E-mail já cadastrado.')
        pass


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    # Function to verify if the file has an allowed extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def cadastro_usuario():
    form = CadastroForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Hash da senha antes de armazená-la
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

        # Create a folder with the user's nome_completo
        user_folder = os.path.join(UPLOADS_FOLDER, form.nome_completo.data)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        # Handle the uploaded files
        filenames = []
        for file in request.files.getlist('identificacao'):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(user_folder, filename)  # Save the file in the user's folder
                file.save(file_path)
                filenames.append(filename)

        # Store the list of filenames in the database
        novo_usuario.identificacao_arquivo = ", ".join(filenames)

        # Verificar se o CPF/CNPJ e o email já estão registrados
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

    return render_template('cadastro2.html', form=form)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
