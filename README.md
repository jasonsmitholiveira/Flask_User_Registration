# Flask User Registration App

Este é um aplicativo de registro de usuário simples desenvolvido com o framework Flask. Ele permite que os usuários se cadastrem com um e-mail e uma senha e armazena os detalhes dos usuários em um banco de dados SQLite.

## Recursos

- Registro de usuário com validação de e-mail e senha.
- Senhas armazenadas no banco de dados como hashes para segurança.
- Verificação de duplicatas de e-mail no banco de dados.
- Funcionalidade básica de login e logout.

## Pré-requisitos

Antes de executar o aplicativo, certifique-se de ter as seguintes dependências instaladas:

- Python 3.x
- Flask
- Flask-WTF
- WTForms
- SQLAlchemy
- Flask-Migrate
- Werkzeug

Você pode instalar essas dependências usando o `pip`:

```bash
pip install Flask Flask-WTF WTForms SQLAlchemy Flask-Migrate Werkzeug
```

Configuração

    Clone o repositório:

bash

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

    Configure sua chave secreta:

No arquivo app.py, substitua 'your_secret_key_here' pela sua chave secreta para segurança da aplicação.

    Configure a URI do banco de dados:

No arquivo app.py, substitua 'sqlite:///your_database.db' pelo caminho do seu banco de dados SQLite.
Uso

Execute o aplicativo usando o seguinte comando:

bash

python app.py

O aplicativo estará disponível em http://localhost:8000/.
Estrutura do Banco de Dados

O aplicativo utiliza um banco de dados SQLite para armazenar os detalhes dos usuários. A tabela User é criada automaticamente com as seguintes colunas:

    id (Chave primária)
    email (E-mail do usuário)
    senha (Hash da senha do usuário)

Contribuição

Sinta-se à vontade para contribuir para este projeto. Você pode abrir problemas (issues) ou enviar pull requests com melhorias e correções.
Licença

Este projeto está licenciado sob a MIT License.

Nota: Este é um aplicativo de demonstração simples e pode precisar de melhorias e recursos adicionais para uso em um ambiente de produção. Certifique-se de seguir as melhores práticas de segurança e considerar a escalabilidade ao adaptar este aplicativo para fins reais.

javascript


Lembre-se de substituir `seu-usuario` e `seu-repositorio` pelos seus detalhes de usuário e repositório do GitHub. Além disso, inclua o arquivo `LICENSE` correspondente se desejar especificar uma licença diferente. Certifique-se de personalizar o README conforme necessário para atender às necessidades do seu projeto.
