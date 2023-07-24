// script.js

// Function to close messages after a certain time
function closeMessages() {
  const messages = document.getElementsByClassName('message');

  for (let i = 0; i < messages.length; i++) {
    const message = messages[i];

    // Use setTimeout to hide the message after 3000 milliseconds (3 seconds)
    setTimeout(() => {
      message.style.display = 'none';
    }, 3000);
  }
}

// Call the function to close messages when the window loads
window.onload = closeMessages;
