// close flash message
const flashMessage = document.querySelector('.flash');
const flashClose = document.querySelector('.flash-close');

if (flashMessage) {
  flashClose.addEventListener('click', () => {
    flashMessage.style.opacity = '0';
    setTimeout(() => {
      flashMessage.remove();
    }, 500);
  });
}