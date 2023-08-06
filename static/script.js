$(document).ready(function () {
    // Function to fetch address data when the user enters the CEP
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

let isValidCpfCnpj = false;

$("#cpf_cnpj").keyup(function () {
    const inputField = $(this);
    const cpfCnpj = inputField.val().replace(/\D/g, '');
    isValidCpfCnpj = cpfCnpj.length === 11 || cpfCnpj.length === 14;

    if (isValidCpfCnpj) {
        inputField.addClass("is-valid").removeClass("is-invalid");
        $("#cpfStatus").html("");
    } else {
        inputField.removeClass("is-valid").addClass("is-invalid");
        $("#cpfStatus").html("");
    }
});

// Check CPF/CNPJ validation on blur event (when the user leaves the input field)
$("#cpf_cnpj").blur(function () {
    const inputField = $(this);
    if (!isValidCpfCnpj) {
        inputField.removeClass("is-valid").addClass("is-invalid");
        $("#cpfStatus").html(`<div class="alert alert-danger">Revise o campo, digite apenas números.</div>`);
    }
});



    // Function to show the modal
    function showTermosModal() {
       // Get user input
    var nome_completo = $("#nome_completo").val();
    var cpf_cnpj = $("#cpf_cnpj").val();
    var endereco_logradouro = $("input[name='endereco_logradouro']").val();
    var endereco_numero = $("input[name='endereco_numero']").val();
    var endereco_bairro = $("input[name='endereco_bairro']").val();
    var endereco_cidade = $("input[name='endereco_cidade']").val();
    var endereco_estado = $("input[name='endereco_estado']").val();
    var endereco_cep = $("#cep").val();

        // Modal content
        const modalContent = `
        <div class="modal fade" id="modalTermos" tabindex="-1" aria-labelledby="modalTermosLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modalTermosLabel">Termos de Serviço</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                    <h1>Termos de Serviço </h1>
    <p>Pelo presente instrumento, as partes aqui qualificadas, de um lado, como LOCADOR, José Calazans Abrantes Júnior,
    doravante denominado simplesmente LOCADOR, e de outro lado, como LOCATÁRIO,
        ${nome_completo}, portador do CPF ${cpf_cnpj}, residente à ${endereco_logradouro}, ${endereco_numero},
        ${endereco_bairro}, ${endereco_cidade}/${endereco_estado}, CEP: ${endereco_cep},
        doravante denominado simplesmente LOCATÁRIO, têm entre si justo e acordado os seguintes Termos de Serviço para o
        aluguel de equipamentos destinados às práticas de esportes outdoors, camping, trilhas e travessias:</p>

    <h2>1. Objeto do Contrato</h2>
    <p>1.1. O LOCADOR disponibiliza ao LOCATÁRIO o aluguel dos equipamentos esportivos destinados a atividades ao ar
        livre, incluindo, mas não se limitando a: barracas de camping, mochilas, isolantes térmicos, fogareiros, entre
        outros, conforme especificações e quantidades discriminadas em contrato específico.</p>

    <h2>2. Elegibilidade</h2>
    <p>2.1. O LOCATÁRIO deverá ter no mínimo 18 anos de idade para utilizar os serviços de aluguel, ou, quando menor de
        idade, contar com a supervisão de um adulto responsável devidamente identificado.</p>
    <p>2.2. Nossos serviços de aluguel estão disponíveis apenas para residentes dentro do território brasileiro.</p>

    <h2>3. Responsabilidades do LOCATÁRIO</h2>
    <p>3.1. O LOCATÁRIO é o único responsável pela utilização adequada dos equipamentos alugados, comprometendo-se a
        utilizá-los de forma segura e em conformidade com as instruções fornecidas pelo LOCADOR.</p>
    <p>3.2. O LOCATÁRIO assume total responsabilidade por quaisquer danos causados aos equipamentos durante o período de
        locação e concorda em reparar ou substituir os itens danificados por outros idênticos ou equivalentes, conforme
        precificação estabelecida pelo LOCADOR.</p>
    <p>3.3. É de responsabilidade do LOCATÁRIO zelar pelos equipamentos alugados e utilizar técnicas eficazes para
        preservar sua integridade, devendo respeitar as especificações e finalidades para as quais foram destinados.</p>

    <h2>4. Limitação de Responsabilidade</h2>
    <p>4.1. O LOCADOR não se responsabiliza por quaisquer perdas, danos ou lesões decorrentes do uso dos equipamentos
        alugados, sendo de inteira responsabilidade do LOCATÁRIO a participação em atividades esportivas ao ar livre,
        camping, trilhas e travessias, que podem conter riscos inerentes.</p>

    <h2>5. Modificações nos Termos de Serviço</h2>
    <p>5.1. O LOCADOR reserva-se o direito de fazer alterações nos presentes Termos de Serviço e notificará os
        LOCATÁRIOS sobre quaisquer modificações. O uso continuado dos serviços após a notificação das alterações constitui
        aceitação dos termos de uso atualizados.</p>

    <h2>6. Encerramento da Locação</h2>
    <p>6.1. O LOCATÁRIO pode encerrar a locação dos equipamentos a qualquer momento, desde que respeite as condições
        estabelecidas no contrato de locação e faça a devida devolução dos equipamentos em bom estado de conservação.</p>


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
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        </div>
        `;

        // Insert the modal in the body of the document
        $("body").append(modalContent);

        // Show the modal
        $("#modalTermos").modal("show");
    }

    // Bind the function to show the modal to the button click
    $("#btnTermos").click(showTermosModal);
});

