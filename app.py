from flask import Flask, render_template, request

app = Flask(__name__)

codigo = 1
pecas = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar_peca', methods=['GET', 'POST'])
def cadastrar_peca():
    global codigo

    if request.method == 'POST':
        nome = request.form['nome']
        fabricante = request.form['fabricante']
        valor = float(request.form['valor'])

        peca = {"codigo": codigo, "nome": nome, "fabricante": fabricante, "valor": valor}
        pecas.append(peca)

        codigo += 1

        return render_template('cadastrar_peca.html', message='Peça cadastrada com sucesso!')

    return render_template('cadastrar_peca.html')

@app.route('/consultar_peca', methods=['GET', 'POST'])
def consultar_peca():
    if request.method == 'POST':
        opcao = request.form['opcao']

        if opcao == '1':
            if len(pecas) == 0:
                return render_template('consultar_peca.html', message='Não há peças cadastradas.', pecas=pecas)
            else:
                return render_template('consultar_peca.html', pecas=pecas)
        elif opcao == '2':
            codigo = int(request.form['codigo'])
            encontrou = False

            # Procurar peça por código
            for peca in pecas:
                if peca["codigo"] == codigo:
                    return render_template('consultar_peca.html', pecas=[peca], editar=True)
                    encontrou = True
                    break

            if not encontrou:
                return render_template('consultar_peca.html', message='Peça não encontrada.', pecas=pecas)
        elif opcao == '3':
            fabricante = request.form['fabricante']
            encontrou = False
            pecas_fabricante = []

            # Procurar peças por fabricante
            for peca in pecas:
                if peca["fabricante"].lower() == fabricante.lower():
                    pecas_fabricante.append(peca)
                    encontrou = True

            if not encontrou:
                return render_template('consultar_peca.html', message='Nenhuma peça encontrada para este fabricante.', pecas=pecas)

            return render_template('consultar_peca.html', pecas=pecas_fabricante)

    return render_template('consultar_peca.html')

@app.route('/remover_peca', methods=['GET', 'POST'])
def remover_peca():
    if request.method == 'POST':
        codigo = int(request.form['codigo'])
        encontrou = False

        for peca in pecas:
            if peca["codigo"] == codigo:
                pecas.remove(peca)
                encontrou = True
                return render_template('remover_peca.html', message='Peça removida com sucesso!')

        if not encontrou:
            return render_template('remover_peca.html', message='Peça não encontrada.')

    return render_template('remover_peca.html')

if __name__ == '__main__':
    app.run(debug=True)
