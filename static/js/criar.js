// Importando a biblioteca Three.js
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.module.js';

// Seleciona o canvas correto
const canvas = document.querySelector("#sandbox-canvas");
const canvasContainer = document.querySelector('.canvas-container');

// Configura a cena 3D
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, canvasContainer.clientWidth / canvasContainer.clientHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: canvas });

// Habilitar sombras
renderer.shadowMap.enabled = true; // Ativar o mapeamento de sombras

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
    model.receiveShadow = true; // O cubo irá receber sombra
    scene.add(model); // Adiciona o cubo à cena

    // Adiciona uma luz direcional para criar sombras
    const light = new THREE.DirectionalLight(0xffffff, 0.5); // Luz branca com intensidade reduzida
    light.position.set(0, 10, 12); // Posição da luz
    light.castShadow = true; // A luz irá projetar sombras

    // Ajustes na sombra
    light.shadow.mapSize.width = 512; // Tamanho da textura da sombra
    light.shadow.mapSize.height = 512; // Tamanho da textura da sombra
    light.shadow.bias = 1; // Ajusta o viés da sombra

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

    // Altera a cor e o tamanho do cubo
    document.querySelector("#color-picker").addEventListener("input", (e) => {
        model.material.color.set(e.target.value); // Altera a cor do cubo
    });

    document.querySelector("#size-input").addEventListener("input", (e) => {
        const scale = e.target.value;
        model.scale.set(scale, scale, scale); // Altera o tamanho do cubo
    });
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
canvas.addEventListener('mousedown', (event) => {
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
