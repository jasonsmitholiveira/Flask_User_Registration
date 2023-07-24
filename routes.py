from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from models import Peca, Cliente

auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)


# Rota para a página de login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Lógica de autenticação - você deve implementar a lógica apropriada aqui.
        # Por exemplo, usar uma biblioteca de autenticação como Flask-Login ou OAuth.
        # Para fins de demonstração, assumiremos uma conta de administrador fixa.
        if username == 'admin' and password == 'password':
            return redirect(url_for('main.index'))  # Redirecionar para a página inicial após o login bem-sucedido
        else:
            return render_template('login.html', message='Credenciais inválidas. Tente novamente.')

    return render_template('login.html')


# Rota para a página de registro
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        address = request.form.get('address')

        # Lógica de registro de usuário - você deve implementar a lógica apropriada aqui.
        # Por exemplo, adicionar um novo usuário ao banco de dados ou integrar com um serviço de autenticação externo.
        # Para fins de demonstração, redirecionaremos para a página de login.
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# Rota para a página inicial
@main_bp.route('/')
def index():
    return render_template('index.html')


# Rota para cadastrar uma nova Peça
@main_bp.route('/cadastrar_peca', methods=['GET', 'POST'])
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


# Rota para consultar as Peças
@main_bp.route('/consultar_peca', methods=['GET', 'POST'])
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


# Rota para remover uma Peça do banco de dados
@main_bp.route('/remover_peca', methods=['GET', 'POST'])
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


# Rota para cadastrar um novo Cliente
@main_bp.route('/cadastrar_cliente', methods=['GET', 'POST'])
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
