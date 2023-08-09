from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('terms.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_email = request.form['user_email']
    user_full_name = request.form['user_full_name']
    user_cpf = request.form['user_cpf']
    user_data_de_nascimento = request.form ['user_data_de_nascimento']
    user_address_logradouro = request.form['user_address_logradouro']
    user_address_numero = request.form['user_address_numero']
    user_address_bairro = request.form['user_address_bairro']
    user_address_cidade = request.form['user_address_cidade']
    user_address_estado = request.form['user_address_estado']
    user_address_cep = request.form['user_address_cep']

    # Crie o conteúdo HTML dos termos de uso
    terms_content = f"""<h1>Termos de Serviço</h1>
                      <p>De um lado, denominado LOCADOR, identificado como José Calazans Abrantes Júnior.</p>
                      <p>De outro lado, denominado LOCATÁRIO, identificado como {user_full_name}, portador do CPF/CNPJ {user_cpf},
                      residente à {user_address_logradouro}, {user_address_numero}, {user_address_bairro}, {user_address_cidade}/{user_address_estado},
                      CEP: {user_address_cep}</p>
<p>Estes Termos de Serviço regulam o aluguel de equipamentos esportivos destinados a atividades ao ar livre, camping, trilhas e travessias:</p>

<h2>1. Objeto do Contrato</h2>
<p>1.1. O LOCADOR disponibiliza para o LOCATÁRIO o aluguel de equipamentos esportivos destinados a atividades ao ar livre, incluindo, mas não limitados a: barracas de camping, mochilas, isolantes térmicos, fogareiros, entre outros.</p>

<h2>2. Elegibilidade</h2>
<p>2.1. O LOCATÁRIO deve ter no mínimo 18 anos de idade para utilizar os serviços de aluguel. Caso o LOCATÁRIO seja menor de idade, é obrigatória a supervisão de um adulto responsável devidamente identificado.</p>
<p>2.2. Nossos serviços de aluguel estão disponíveis exclusivamente para residentes no território brasileiro.</p>

<h2>3. Responsabilidades do LOCATÁRIO</h2>
<p>3.1. O LOCATÁRIO é inteiramente responsável por utilizar os equipamentos alugados de maneira adequada,
    comprometendo-se a empregá-los com segurança e de acordo com as instruções fornecidas pelo fabricante do equipamento alugado.</p>
<p>3.2. É obrigação do LOCATÁRIO zelar pela conservação dos equipamentos alugados, empregando métodos eficazes
    para a sua preservação e aderindo às especificações de uso e finalidade estabelecidas.</p>
<p>3.3. Caso o equipamento sofra algum dano que o LOCADOR considere que prejudique o seu uso, e isso seja verificado após a entrega dos itens alugados ou informado pelo LOCATÁRIO,
    o LOCATÁRIO precisa fazer uma destas ações: comprar o mesmo equipamento danificado ou similar, seguindo o preço atual da loja <a href="https://lojaam.com.br">altamontanha</a>,
    ou efetuar o pagamento correspondente ao valor atual do item danificado ao LOCADOR, dentro do prazo legal de 30 (trinta) dias a partir da data de comunicação do dano.</p>
<p>3.4. No caso de o produto não estiver disponível na loja altamontanha, o LOCATÁrio deverá efetuar o pagamento correspondente ao valor atual do item danificado ao LOCADOR, considerando o valor de mercado de equipamentos semelhantes disponíveis em outras lojas de venda online, excluindo Marketplaces como MercadoLivre ou similares, dentro do prazo legal de 30 (trinta) dias a partir da data de comunicação do dano.</p>
<p>3.5. Caso o pagamento não seja efetuado no prazo estabelecido, o LOCADOR reserva-se o direito de adotar as seguintes medidas:</p>
<ul>
    <li>Cobrança de juros de mora e correção monetária, conforme previsto em lei;</li>
    <li>Registro do LOCATÁRIO em órgãos de proteção ao crédito;</li>
    <li>Busca de acordo amigável para regularização da pendência;</li>
    <li>Caso necessário, ação judicial para cobrança dos valores devidos, com todas as despesas legais e custas judiciais a cargo do LOCATÁRIO.</li>
</ul>

<h2>4. Limitação de Responsabilidade</h2>
<p>4.1. O LOCADOR não assume responsabilidade por quaisquer perdas, danos ou lesões resultantes do uso dos
    equipamentos alugados. A participação em atividades esportivas ao ar livre, camping, trilhas e
    travessias, sujeitas a riscos inerentes, é inteiramente de responsabilidade do LOCATÁRIO.</p>

<h2>5. Alterações nos Termos de Serviço</h2>
<p>5.1. O LOCADOR reserva-se o direito de efetuar alterações nestes Termos de Serviço e
    comunicará aos LOCATÁRIOS quaisquer modificações. O uso continuado dos serviços após a notificação
    implica na aceitação dos termos atualizados.</p>

<h2>6. Encerramento da Locação</h2>
<p>6.1. O LOCATÁRIO tem o direito de encerrar a locação dos equipamentos a qualquer momento, realizando a devolução adequada dos
    equipamentos, mantendo-os em bom estado de conservação.</p>
    <p>6.2. É importante ressaltar que, em caso de encerramento antecipado da locação pelo LOCATÁRIO, <strong style="color: red;">não haverá devolução do valor pago </strong> pelo período de locação originalmente contratado.</p>

<h2>7. Devolução dos Equipamentos</h2>
<p>7.1. O LOCATÁRIO compromete-se a devolver os equipamentos alugados na data de entrega prevista, conforme acordado com o Locador.</p>
<p>7.2. Caso o LOCATÁRIO não devolva os equipamentos na data acordada, será aplicada uma <strong style="color: red;">taxa diária de atraso, de 100%</strong></p>
<p>7.3. Se os equipamentos não forem devolvidos após um período de atraso superior a 2 dias, o LOCADOR reserva-se o direito de tomar medidas legais para recuperar os equipamentos e/ou os valores correspondentes ao atraso.</p>
<p>7.4. Se os equipamentos não forem devolvidos mesmo após notificações e tentativas de resolução, o LOCADOR poderá acionar as autoridades policiais para relatar o não cumprimento do contrato e buscar a devolução dos equipamentos, bem como acionar medidas judiciais para buscar ressarcimento pelos danos causados.</p>
<p>7.5. Em caso de acionamento judicial, todas as despesas legais e custas judiciais serão de responsabilidade do LOCATÁRIO.</p>
<p>7.6. O LOCADOR também pode entrar em contato com o LOCATÁRIO para estabelecer um acordo de extensão do prazo de locação, sujeito a termos adicionais.</p>
<p>7.7. No caso de devolução dos equipamentos após um período de atraso, o LOCADOR fará uma avaliação do estado dos equipamentos e poderá aplicar taxas adicionais para reparos ou substituição, conforme necessário.</p>



    <h1>Política de Privacidade:</h1>
    <p>Coleta de Dados: José Calazans Abrantes Júnior coleta dados pessoais dos usuários apenas para fins relacionados à locação dos equipamentos. Os dados fornecidos pelo usuário serão utilizados somente para a finalidade específica e não serão compartilhados com terceiros sem autorização.</p>
    <p>Uso dos Dados: Os dados pessoais coletados serão utilizados para processar as solicitações de locação, fornecer suporte ao cliente e melhorar nossos serviços. Não utilizaremos os dados para fins de marketing sem o consentimento explícito do usuário.</p>
    <p>Armazenamento e Segurança: José Calazans Abrantes Júnior tomará medidas adequadas para proteger os dados pessoais dos usuários contra acesso não autorizado, perda, divulgação ou alteração. Os dados serão armazenados de forma segura e apenas pelo tempo necessário para cumprir as finalidades para as quais foram coletados.</p>
    <p>Cookies e Tecnologias de Rastreamento: José Calazans Abrantes Júnior poderá utilizar cookies e tecnologias de rastreamento para melhorar a experiência do usuário, fornecer conteúdo personalizado e analisar o uso do nosso site. O usuário pode gerenciar as preferências de cookies do seu navegador, mas desativar os cookies pode afetar algumas funcionalidades do site.</p>
    <p>Links para Terceiros: Nosso site pode conter links para sites de terceiros. Esta Política de Privacidade se aplica somente ao nosso site, não sendo nossa responsabilidade o conteúdo ou as práticas de privacidade desses sites externos.</p>

    <h1>Uso de Cookies:</h1>
    <p>O que são Cookies: Cookies são pequenos arquivos de texto que são armazenados no seu dispositivo quando você visita um site. Eles contêm informações sobre a sua visita e podem ser úteis para melhorar a experiência do usuário.</p>
    <p>Como Utilizamos os Cookies: José Calazans Abrantes Júnior utiliza cookies para entender como os usuários interagem com o nosso site, personalizar conteúdo e anúncios, fornecer recursos de mídia social e analisar padrões de tráfego. Isso nos ajuda a melhorar nossos serviços e oferecer uma experiência mais relevante aos usuários.</p>
    <p>Gerenciamento de Cookies: Você pode gerenciar as preferências de cookies do seu navegador, permitindo, bloqueando ou excluindo os cookies. No entanto, desativar os cookies pode afetar algumas funcionalidades do site.</p>
    <p>Cookies de Terceiros: Nossos parceiros de publicidade e análise também podem usar cookies em nosso site. Esses cookies são regidos pelas políticas de privacidade de terceiros, e não temos controle sobre eles.</p>

    <p>Ao utilizar os serviços de aluguel de equipamentos de José Calazans Abrantes Júnior, você concorda com os Termos de Serviço, a Política de Privacidade e o Uso de Cookies aqui estabelecidos. É importante ler e compreender completamente estes documentos antes de utilizar nossos serviços.</p>
"""

    # Configurações do servidor de e-mail (Exemplo: Gmail)
    email_servidor = 'gotrekbrasil@gmail.com'  # Coloque o seu endereço de e-mail
    email_senha = 'yeixpnjesuqvarvs'  # Coloque sua senha do e-mail
    smtp_servidor = 'smtp.gmail.com'
    smtp_porta = 587

    # Configure e envie o e-mail
    try:
        smtp_server = smtplib.SMTP(smtp_servidor, smtp_porta)
        smtp_server.starttls()
        smtp_server.login(email_servidor, email_senha)

        msg = MIMEMultipart()
        msg['From'] = email_servidor
        msg['To'] = user_email
        msg['Subject'] = 'Assinatura dos Termos de Serviço'

        msg.attach(MIMEText(terms_content, 'html'))

        smtp_server.sendmail(email_servidor, user_email, msg.as_string())
        smtp_server.quit()

        return 'E-mail enviado com sucesso!'
    except Exception as e:
        return f'Erro ao enviar o e-mail: {str(e)}'


if __name__ == '__main__':
    app.run(debug=True)
