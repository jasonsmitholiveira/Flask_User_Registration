from flask import Flask, render_template, request, Blueprint
from flask_sqlalchemy import SQLAlchemy

app1 = Flask(__name__)

# Criação do Blueprint
blueprint1 = Blueprint('app1', __name__)

# Configurando o banco de dados SQLite
app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app1)


# Criando o modelo do banco de dados para Peca (peça) e Cliente (cliente)
class Peca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
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

# Função para criar as tabelas do banco de dados
def create_tables():
    with app1.app_context():
        db.create_all()


# Rota para a página inicial
@app1.route('/')
def index():
    return render_template('index.html')


# Rota para cadastrar uma nova Peca (peça)
@app1.route('/cadastrar_peca', methods=['GET', 'POST'])
def cadastrar_peca():
    if request.method == 'POST':
        nome = request.form.get('nome')
        fabricante = request.form.get('fabricante')
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')

        # Verificando se todos os campos estão preenchidos
        if not nome or not fabricante or not descricao or not valor:
            return render_template('error.html', message='Preencha todos os campos para cadastrar a peça.')

        try:
            valor = float(valor)
        except ValueError:
            return render_template('error.html', message='O valor precisa ser um número válido.')

        # Criando um novo objeto Peca e adicionando-o ao banco de dados
        peca = Peca(nome=nome, fabricante=fabricante, descricao=descricao, valor=valor)
        db.session.add(peca)

        # Realizando o commit para salvar a nova peça no banco de dados
        db.session.commit()

        return render_template('success.html', message='Peça cadastrada com sucesso!')

    return render_template('cadastrar_peca.html')


# Rota para consultar os dados da Peca (peça)
@app1.route('/consultar_peca', methods=['GET', 'POST'])
def consultar_peca():
    if request.method == 'POST':
        opcao = request.form.get('opcao')

        if opcao == '1':
            # Obtendo todas as peças do banco de dados
            pecas = Peca.query.all()

            return render_template('consultar_peca.html', pecas=pecas)

        elif opcao == '2':
            codigo = request.form.get('codigo')
            if not codigo:
                return render_template('error.html', message='Digite um código para consultar a peça.')

            try:
                codigo = int(codigo)
            except ValueError:
                return render_template('error.html', message='O código precisa ser um número válido.')

            # Obtendo uma peça específica do banco de dados com base no código fornecido
            peca = Peca.query.get(codigo)
            if not peca:
                return render_template('error.html', message='Peça não encontrada.')

            return render_template('consultar_peca.html', pecas=[peca], editar=True)

        elif opcao == '3':
            fabricante = request.form.get('fabricante')
            if not fabricante:
                return render_template('error.html', message='Digite um fabricante para consultar as peças.')

            # Obtendo todas as peças do banco de dados com base no fabricante fornecido
            pecas = Peca.query.filter(Peca.fabricante.ilike(fabricante)).all()

            return render_template('consultar_peca.html', pecas=pecas)

    return render_template('consultar_peca.html')


# Rota para remover uma Peca (peça) do banco de dados
@app1.route('/remover_peca', methods=['GET', 'POST'])
def remover_peca():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        if not codigo:
            return render_template('error.html', message='Digite um código para remover a peça.')

        try:
            codigo = int(codigo)
        except ValueError:
            return render_template('error.html', message='O código precisa ser um número válido.')

        # Obtendo o objeto Peca a ser removido do banco de dados com base no código fornecido
        peca = Peca.query.get(codigo)
        if not peca:
            return render_template('error.html', message='Peça não encontrada.')

        # Removendo o objeto Peca do banco de dados
        db.session.delete(peca)
        db.session.commit()

        return render_template('success.html', message='Peça removida com sucesso!')

    return render_template('remover_peca.html')


# Rota para cadastrar um novo Cliente (cliente)
@app1.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome_completo = request.form.get('nome_completo')
        endereco_completo = request.form.get('endereco_completo')
        email = request.form.get('email')
        telefone = request.form.get('telefone')

        # Verificando se todos os campos estão preenchidos
        if not nome_completo or not endereco_completo or not email or not telefone:
            return render_template('error.html', message='Preencha todos os campos para cadastrar o cliente.')

        # Verificando se um cliente com o mesmo email já existe no banco de dados
        cliente_existente = Cliente.query.filter_by(email=email).first()
        if cliente_existente:
            return render_template('error.html', message='Este email já está cadastrado.')

        # Criando um novo objeto Cliente e adicionando-o ao banco de dados
        cliente = Cliente(nome_completo=nome_completo, endereco_completo=endereco_completo,
                          email=email, telefone=telefone)

        db.session.add(cliente)
        db.session.commit()

        return render_template('success.html', message='Cadastro realizado com sucesso!')

    return render_template('cadastrar_cliente.html')


if __name__ == '__main__':
    # Criando as tabelas do banco de dados antes de executar a aplicação
    create_tables()
    app1.run(debug=True)
