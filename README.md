# Cadastro de Usuário - Flask Web App

Este é um projeto de aplicação web desenvolvido com Flask, um framework web em Python, que permite cadastrar usuários e armazenar suas informações em um banco de dados SQLite. O projeto inclui um formulário de cadastro com validações de campos, upload de arquivos e interação com API externa para buscar informações de endereço a partir do CEP informado.

## Funcionalidades

- Cadastro de usuário com os seguintes campos:
  - CPF/CNPJ (com validação de 11 ou 14 números, somente números);
  - Nome Completo;
  - Data de Nascimento;
  - Gênero (opções: masculino, feminino e outros);
  - Estado Civil (opções: solteiro, casado e outros);
  - E-mail (com validação de e-mail válido e não duplicado);
  - Telefone (com validação de 11 números, DDD + número do telefone, juntos);
  - Senha (com validação de confirmação de senha);
  - Endereço (CEP, Logradouro, Número, Complemento, Bairro, Cidade e Estado);
  - Identificação (upload de arquivo).

- Validações de dados em tempo real utilizando JavaScript e jQuery:
  - Verificação de CPF/CNPJ (11 ou 14 números);
  - Verificação de telefone (11 números).

- Armazenamento seguro das senhas utilizando a biblioteca Werkzeug.

- Verificação de e-mails e CPF/CNPJ já cadastrados para evitar duplicações.

## Pré-requisitos

- Python 3.x
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Werkzeug
- Requests

## Instalação

1. Clone este repositório em sua máquina local:

```bash
git clone https://github.com/joseabrantesjr/SistemaJoseAbrantesJr.git
```

2. Acesse o diretório do projeto:
```bash
cd SistemaJoseAbrantesJr
```

3. Crie e ative um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
# No Windows: venv\Scripts\activate
# No Linux/Mac: source venv/bin/activate
```
4. Instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

5.  Inicie o servidor Flask:
```bash
python app.py
```
6. Acesse a aplicação no navegador em http://localhost:5000/

## Contribuição

Contribuições são bem-vindas! Se você encontrou algum problema, tem sugestões de melhorias ou deseja adicionar novas funcionalidades, fique à vontade para criar um Pull Request.

## Licença

Este projeto não possui licença. Sinta-se à vontade para utilizar e modificar o código de acordo com suas necessidades.