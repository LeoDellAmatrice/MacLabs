document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modal-container');
    const closeModal = document.getElementById('close-modal');

    // Mostra o modal ao carregar a página
    modal.classList.add('visible');
    document.body.style.overflow = 'hidden'; // Impede a rolagem

    // Fecha o modal ao clicar no botão
    closeModal.addEventListener('click', function() {
        modal.classList.remove('visible');
        document.body.style.overflow = ''; // Restaura a rolagem
    });
});
