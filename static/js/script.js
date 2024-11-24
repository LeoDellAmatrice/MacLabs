// Seleciona todas as engrenagens com a classe 'gear'
const gears = document.querySelectorAll('.gear');
const gears2 = document.querySelectorAll('.gear2');

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

gears2.forEach(gear2 => {
    gear2.addEventListener('mouseover', function() {
        // Adiciona a classe que inicia a animação
        gear2.classList.add('rotate');

        // Remove a classe após a animação terminar para permitir uma nova interação
        gear2.addEventListener('animationend', function() {
            gear2.classList.remove('rotate');
        });
    });
});