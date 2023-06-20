// script.js

// Função para fechar as mensagens após um certo tempo
function closeMessages() {
  const messages = document.getElementsByClassName('message');

  for (let i = 0; i < messages.length; i++) {
    const message = messages[i];

    setTimeout(() => {
      message.style.display = 'none';
    }, 3000);
  }
}

// Chama a função para fechar as mensagens ao carregar a página
window.onload = closeMessages;
