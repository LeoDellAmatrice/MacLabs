// Seleciona todas as engrenagens com a classe 'gear'
const gears = document.querySelectorAll('.gear');

gears.forEach(gear => {
    gear.addEventListener('mouseover', function() {
        // Adiciona a classe que inicia a animação
        gear.classList.add('rotate');

        // Remove a classe após a animação terminar para permitir uma nova interação
        gear.addEventListener('animationend', function() {
            gear.classList.remove('rotate');
        });
    });
});