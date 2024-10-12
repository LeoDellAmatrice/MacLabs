// Importando a biblioteca Three.js
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.module.js';

// Seleciona o canvas correto
const canvas = document.querySelector("#sandbox-canvas");
const canvasContainer = document.querySelector('.canvas-container');

// Configura a cena 3D
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, canvasContainer.clientWidth / canvasContainer.clientHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: canvas });

// Habilitar sombras e definir cor de fundo
renderer.shadowMap.enabled = true; // Ativar o mapeamento de sombras
renderer.setClearColor(0x252525, 1); // Define a cor de fundo (exemplo: cinza escuro)

// Definindo preços básicos
const basePricePerCubicCm = 14.00; // Preço por cm³ (ajuste conforme necessário)
const materialPrices = {
    pla: 0.05, // Custo do PLA por cm³
    abs: 0.06, // Custo do ABS por cm³
    petg: 0.07, // Custo do PETG por cm³
    nylon: 0.08 // Custo do Nylon por cm³
};
const baseInfillPrice = 0.01; // Custo adicional por densidade de preenchimento

// Função para ajustar o canvas e a câmera
function ajustarCanvasECamera() {
    const width = canvasContainer.clientWidth;
    const height = canvasContainer.clientHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
}

// Inicializa a cena e o cubo
let model;
let isMouseDown = false;
let previousMousePosition = { x: 0, y: 0 };
let idleTimeout;
const idleTime = 2000;
let animationActive = true;

function initThreeJS() {
    ajustarCanvasECamera();

    // Cria um cubo básico
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshStandardMaterial({ color: 0x2d8ef1 }); // Usar MeshStandardMaterial para sombras
    model = new THREE.Mesh(geometry, material); // Cria o cubo
    model.castShadow = true; // O cubo irá projetar sombra
    scene.add(model); // Adiciona o cubo à cena

    // Cria um plano para receber a sombra
    const planeGeometry = new THREE.PlaneGeometry(500, 500);
    const planeMaterial = new THREE.ShadowMaterial({ opacity: 0.5 });
    const plane = new THREE.Mesh(planeGeometry, planeMaterial);
    plane.rotation.x = -Math.PI / 2; // Deita o plano horizontalmente
    plane.position.y = -1; // Posiciona o plano abaixo do cubo
    plane.receiveShadow = true; // O plano irá receber a sombra
    scene.add(plane);

    // Adiciona uma luz direcional para criar sombras
    const light = new THREE.DirectionalLight(0xffffff, 1); // Luz branca
    light.position.set(0, 10, 12); // Posição da luz
    light.castShadow = true; // A luz irá projetar sombras

    // Ajustes na sombra
    light.shadow.mapSize.width = 1024; // Tamanho da textura da sombra
    light.shadow.mapSize.height = 1024; // Tamanho da textura da sombra
    light.shadow.bias = -0.01; // Ajusta o viés da sombra para evitar deslocamento

    scene.add(light); // Adiciona a luz à cena

    camera.position.z = 5;

    function animate() {
        if (animationActive && model) {
            model.rotation.y += 0.01; // Anima a rotação do cubo
        }
        renderer.render(scene, camera); // Renderiza a cena
        requestAnimationFrame(animate); // Chama a animação novamente
    }

    animate(); // Inicia a animação

    // Atualiza o preço e o tempo estimado
    document.querySelector("#size-input").addEventListener("input", updateEstimations);
    document.querySelector("#material-select").addEventListener("change", updateEstimations);
    document.querySelector("#infill-density").addEventListener("input", updateEstimations);

    // Altera a cor do cubo com base na cor selecionada
    const colorButtons = document.querySelectorAll('.color-option');
    colorButtons.forEach(button => {
        button.addEventListener('click', () => {
            const selectedColor = button.getAttribute('data-color');
            model.material.color.set(selectedColor); // Altera a cor do cubo
            updateEstimations(); // Atualiza as estimativas após mudar a cor
        });
    });
}

// Função para atualizar as estimativas de tempo e preço
function updateEstimations() {
    const scale = document.querySelector("#size-input").value;
    model.scale.set(scale, scale, scale); // Altera o tamanho do cubo

    // Calcula o volume do cubo (lado³)
    const volume = Math.pow(scale, 3); // Volume em cm³
    const estimatedPrice = (volume * basePricePerCubicCm).toFixed(2); // Estima o preço

    // Estima o tempo de impressão em minutos
    const infillDensity = document.querySelector("#infill-density").value; // Obtém a densidade de preenchimento
    const densityFactor = 1 + (infillDensity / 100); // Fator de densidade
    const timePerCubicCm = 10; // Minutos por cm³
    const estimatedTime = Math.max(Math.floor((volume * timePerCubicCm) * densityFactor), 1); // Tempo em minutos

    // Atualiza o texto de preço estimado
    document.querySelector("#estimated-price").textContent = `R$ ${estimatedPrice}`;

    // Atualiza o texto de tempo estimado
    document.querySelector("#estimated-time").textContent = `Aprox. ${estimatedTime} minutos`;

    // Atualiza o preço com base no material e densidade de preenchimento
    const selectedMaterial = document.querySelector("#material-select").value;
    const materialCost = materialPrices[selectedMaterial] * (volume / 100); // Custo do material
    const infillCost = baseInfillPrice * (infillDensity / 5); // Custo baseado na densidade de preenchimento

    const totalPrice = (parseFloat(estimatedPrice) + materialCost + infillCost).toFixed(2);
    document.querySelector("#estimated-price").textContent = `R$ ${totalPrice}`;
}

// Chama a função initThreeJS assim que a janela é carregada
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
    initThreeJS(); // Inicializa a cena 3D
});

// Redimensiona o canvas quando a janela é redimensionada
window.addEventListener('resize', () => {
    ajustarCanvasECamera(); // Ajusta a câmera e o canvas
    renderer.render(scene, camera); // Renderiza novamente após o redimensionamento
});

// Controle de rotação do cubo usando o mouse
canvas.addEventListener('mousedown', () => {
    isMouseDown = true; // Ativa o arraste
    animationActive = false; // Pausa a animação enquanto arrasta
    clearTimeout(idleTimeout); // Limpa o temporizador de inatividade
});

canvas.addEventListener('mousemove', (event) => {
    if (!isMouseDown) return;

    const deltaMove = {
        x: previousMousePosition.x - event.offsetX, // Inverte a rotação Y
        y: previousMousePosition.y - event.offsetY, // Inverte a rotação X
    };

    if (model) {
        model.rotation.y += deltaMove.x * 0.01; // Rotação correta no eixo Y
        model.rotation.x -= deltaMove.y * 0.01; // Inverte a rotação no eixo X
    }

    previousMousePosition = {
        x: event.offsetX,
        y: event.offsetY,
    };

    clearTimeout(idleTimeout);
    idleTimeout = setTimeout(() => {
        animationActive = true; // Retorna à animação após o tempo de inatividade
    }, idleTime);
});

canvas.addEventListener('mouseup', () => {
    isMouseDown = false; // Para a rotação quando o botão do mouse é liberado
});

canvas.addEventListener('mouseleave', () => {
    isMouseDown = false; // Para a rotação quando o mouse sai do canvas
});

// Adiciona controle de touch para dispositivos móveis
canvas.addEventListener('touchstart', (event) => {
    isMouseDown = true; // Ativa o arraste
    animationActive = false; // Pausa a animação enquanto arrasta
    clearTimeout(idleTimeout); // Limpa o temporizador de inatividade
    event.preventDefault(); // Prevê o comportamento padrão do touch
});

canvas.addEventListener('touchmove', (event) => {
    if (!isMouseDown) return;

    const touch = event.touches[0];
    const deltaMove = {
        x: previousMousePosition.x - touch.clientX,
        y: previousMousePosition.y - touch.clientY,
    };

    if (model) {
        model.rotation.y += deltaMove.x * 0.01; // Rotação correta no eixo Y
        model.rotation.x -= deltaMove.y * 0.01; // Inverte a rotação no eixo X
    }

    previousMousePosition = {
        x: touch.clientX,
        y: touch.clientY,
    };

    clearTimeout(idleTimeout);
    idleTimeout = setTimeout(() => {
        animationActive = true; // Retorna à animação após o tempo de inatividade
    }, idleTime);

    event.preventDefault(); // Prevê o comportamento padrão do touch
});

canvas.addEventListener('touchend', () => {
    isMouseDown = false; // Para a rotação quando o toque termina
});
