window.addEventListener('load', function() {
    document.body.classList.add('loaded');

    // Exibir o modal
    const modal = document.getElementById('modal-aviso');
    const closeButton = document.querySelector('.close-button');

    modal.style.display = 'block';

    // Função para fechar o modal quando o usuário clicar no 'x'
    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Fechar o modal se o usuário clicar fora do conteúdo
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});
