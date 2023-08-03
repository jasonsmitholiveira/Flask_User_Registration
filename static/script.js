
  $(document).ready(function () {
    // Conteúdo do modal
    const modalContent = `
    <div class="modal fade" id="modalTermos" tabindex="-1" aria-labelledby="modalTermosLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-scrollable">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="modalTermosLabel">Termos de Serviço</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                        <h1>Termos de Serviço:</h1>
    <p>Ao utilizar os serviços de aluguel de equipamentos para esportes outdoors, camping, trilhas, disponibilizados por José Calazans Abrantes Júnior, pessoa física, o usuário concorda em respeitar e cumprir estes Termos de Serviço.</p>
    <ul>
        <li>Elegibilidade: O usuário deve ter pelo menos 18 anos de idade para utilizar nossos serviços ou contar com a supervisão de um adulto responsável. Nossos serviços estão disponíveis apenas para residentes dentro do território brasileiro.</li>
        <li>Responsabilidades do Usuário: O usuário é o único responsável pela utilização dos equipamentos locados e deve utilizá-los de forma segura, em conformidade com as instruções de utilização. O usuário assume total responsabilidade por qualquer dano causado ao equipamento durante o período de locação e concorda em comprar outro item idêntico ou equivalente ao preço atual do item em caso de danos que comprometam a usabilidade do equipamento alugado.</li>
        <li>Zelo pelos Equipamentos: O usuário deve zelar pelos equipamentos alugados e utilizar técnicas eficazes para preservar sua integridade. Os equipamentos devem ser utilizados de acordo com as especificações e finalidades para as quais são destinados.</li>
        <li>Limitação de Responsabilidade: José Calazans Abrantes Júnior não se responsabiliza por quaisquer perdas, danos ou lesões decorrentes do uso dos equipamentos alugados. O usuário reconhece que atividades esportivas outdoors, camping, trilhas podem conter riscos inerentes e que sua participação é de sua inteira responsabilidade.</li>
        <li>Modificações nos Termos de Serviço: José Calazans Abrantes Júnior reserva-se o direito de fazer alterações nestes Termos de Serviço e notificará os usuários sobre qualquer modificação. O uso continuado dos serviços após a notificação das alterações constitui aceitação dos termos de uso atualizados.</li>
        <li>Encerramento da Locação: O usuário pode encerrar a locação dos equipamentos a qualquer momento, respeitando as condições estabelecidas no contrato de locação.</li>
    </ul>

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

    <p>Ao utilizar os serviços de aluguel de equipamentos de José Calazans Abrantes Júnior, pessoa física, você concorda com os Termos de Serviço, a Política de Privacidade e o Uso de Cookies aqui estabelecidos. É importante ler e compreender completamente estes documentos antes de utilizar nossos serviços.</p>
    </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
            </div>
          </div>
        </div>
      </div>
    `;

        // Inserir o modal no corpo do documento
    $("body").append(modalContent);

    // Função para exibir o modal
    function showTermosModal() {
      $("#modalTermos").modal("show");
    }

    // Vincular a função de exibição do modal ao clique do botão
    $("#btnTermos").click(showTermosModal);
  });

    $(document).ready(function () {
        // Fetch address data when the user enters the CEP
        $("#cep").blur(function () {
            const cep = $(this).val().replace(/\D/g, '');

            if (cep.length === 8) {
                fetch(`https://viacep.com.br/ws/${cep}/json/`)
                    .then(response => response.json())
                    .then(data => {
                        $("#endereco_logradouro").val(data.logradouro);
                        $("#endereco_bairro").val(data.bairro);
                        $("#endereco_cidade").val(data.localidade);
                        $("#endereco_estado").val(data.uf);
                    });
            }
        });

        // Display the verification code input field after successful registration
        {% if messages %}
            {% if 'Cadastro realizado com sucesso' in messages %}
                $("#verificationCodeDiv").show();
            {% endif %}
        {% endif %}
    });

    $(document).ready(function() {
        // Função para verificar o CPF em tempo real
        $("#cpf_cnpj").keyup(function() {
            const cpf = $(this).val().replace(/\D/g, '');
            const data_nascimento = $("#data_nascimento").val();

            // Verificar se o CPF possui 11 dígitos e se a data de nascimento está preenchida
            if (cpf.length === 11 && data_nascimento) {
                $.ajax({
                    url: "/verificar_cpf",
                    type: "POST",
                    data: {
                        cpf_cnpj: cpf,
                        data_nascimento: data_nascimento
                    },
                    success: function (response) {
                        if (response.status === "success") {
                            $("#cpfStatus").html(`<div class="alert alert-success">Situação cadastral: Regular</div>`);
                            // Caso queira preencher automaticamente o nome completo:
                            // $("#nome_completo").val(response.nome_completo);
                        } else {
                            $("#cpfStatus").html(`<div class="alert alert-danger">${response.message}</div>`);
                        }
                    },
                    error: function () {
                        $("#cpfStatus").html(`<div class="alert alert-danger">Erro ao verificar o CPF.</div>`);
                    }
                });
            } else {
                $("#cpfStatus").html("");
            }
        });
    });

    $(document).ready(function () {
        // Função para verificar o CPF/CNPJ em tempo real
        $("#cpf_cnpj").keyup(function () {
            var cpf_cnpj = $(this).val().replace(/\D/g, '');

            if (cpf_cnpj.length === 11 || cpf_cnpj.length === 14) {
                // CPF/CNPJ possui 11 ou 14 números, removemos a mensagem de erro (se houver) e adicionamos a classe 'is-valid'
                $(this).removeClass('is-invalid').addClass('is-valid');
            } else {
                // CPF/CNPJ não possui 11 ou 14 números, adicionamos a classe 'is-invalid' para mostrar a mensagem de erro
                $(this).removeClass('is-valid').addClass('is-invalid');
            }
        });

        // Função para verificar o telefone em tempo real
        $("#telefone").keyup(function () {
            var telefone = $(this).val().replace(/\D/g, '');

            if (telefone.length === 11) {
                // O telefone possui 11 números, removemos a mensagem de erro (se houver) e adicionamos a classe 'is-valid'
                $(this).removeClass('is-invalid').addClass('is-valid');
            } else {
                // O telefone não possui 11 números, adicionamos a classe 'is-invalid' para mostrar a mensagem de erro
                $(this).removeClass('is-valid').addClass('is-invalid');
            }
        });
    });
