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
renderer.shadowMap.enabled = true;
renderer.setClearColor(0x252525, 1);

// Definindo preços básicos
const basePricePerCubicCm = 5.00;
const materialPrices = {
    pla: 0.05,
    abs: 0.06,
    petg: 0.07,
    nylon: 0.08
};
const baseInfillPrice = 0.01;

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

    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshStandardMaterial({ color: 0x2d8ef1 });
    model = new THREE.Mesh(geometry, material);
    model.castShadow = true;
    scene.add(model);

    const planeGeometry = new THREE.PlaneGeometry(500, 500);
    const planeMaterial = new THREE.ShadowMaterial({ opacity: 0.5 });
    const plane = new THREE.Mesh(planeGeometry, planeMaterial);
    plane.rotation.x = -Math.PI / 2;
    plane.position.y = -1;
    plane.receiveShadow = true;
    scene.add(plane);

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(0, 10, 12);
    light.castShadow = true;
    light.shadow.mapSize.width = 1024;
    light.shadow.mapSize.height = 1024;
    light.shadow.bias = -0.01;

    scene.add(light);

    camera.position.z = 5;

    function animate() {
        if (animationActive && model) {
            model.rotation.y += 0.01;
        }
        renderer.render(scene, camera);
        requestAnimationFrame(animate);
    }

    animate();

    // Atualiza o preço e o tempo estimado
    const sizeInput = document.querySelector("#size-input");
    const infillInput = document.querySelector("#infill-density");
    const sizeValueDisplay = document.querySelector("#size-value");
    const infillValueDisplay = document.querySelector("#infill-value");

    sizeInput.addEventListener("input", () => {
        sizeValueDisplay.textContent = sizeInput.value; // Exibe o valor atual do tamanho
        updateEstimations();
    });
    infillInput.addEventListener("input", () => {
        infillValueDisplay.textContent = `${infillInput.value}%`; // Exibe o valor atual da densidade
        updateEstimations();
    });

    document.querySelector("#material-select").addEventListener("change", updateEstimations);

    const colorButtons = document.querySelectorAll('.color-option');
    colorButtons.forEach(button => {
        button.addEventListener('click', () => {
            const selectedColor = button.getAttribute('data-color');
            model.material.color.set(selectedColor);
            updateEstimations();
        });
    });
}

// Função para atualizar as estimativas de tempo e preço
function updateEstimations() {
    const scale = document.querySelector("#size-input").value;
    model.scale.set(scale, scale, scale);

    const volume = Math.pow(scale, 3);
    const infillDensity = document.querySelector("#infill-density").value;
    const densityFactor = 1 + (infillDensity / 100);
    const timePerCubicCm = 10;
    const estimatedTime = Math.max(Math.floor((volume * timePerCubicCm) * densityFactor), 1);

    document.querySelector("#estimated-time").textContent = `Aprox. ${estimatedTime} minutos`;

    const selectedMaterial = document.querySelector("#material-select").value;
    const materialCost = materialPrices[selectedMaterial] * (volume / 100);
    const infillCost = baseInfillPrice * (infillDensity / 5);
    const estimatedPrice = (volume * basePricePerCubicCm + materialCost + infillCost).toFixed(2);

    document.querySelector("#estimated-price").textContent = `R$ ${estimatedPrice}`;
}

// Chama a função initThreeJS assim que a janela é carregada
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
    initThreeJS();
});

window.addEventListener('resize', () => {
    ajustarCanvasECamera();
    renderer.render(scene, camera);
});

// Controle de rotação do cubo usando o mouse e touch
canvas.addEventListener('mousedown', () => {
    isMouseDown = true;
    animationActive = false;
    clearTimeout(idleTimeout);
});

canvas.addEventListener('mousemove', (event) => {
    if (!isMouseDown) return;

    const deltaMove = {
        x: previousMousePosition.x - event.offsetX,
        y: previousMousePosition.y - event.offsetY,
    };

    if (model) {
        model.rotation.y += deltaMove.x * 0.01;
        model.rotation.x -= deltaMove.y * 0.01;
    }

    previousMousePosition = {
        x: event.offsetX,
        y: event.offsetY,
    };

    clearTimeout(idleTimeout);
    idleTimeout = setTimeout(() => {
        animationActive = true;
    }, idleTime);
});

canvas.addEventListener('mouseup', () => {
    isMouseDown = false;
});

canvas.addEventListener('mouseleave', () => {
    isMouseDown = false;
});

canvas.addEventListener('touchstart', (event) => {
    isMouseDown = true;
    animationActive = false;
    clearTimeout(idleTimeout);
    event.preventDefault();
});

canvas.addEventListener('touchmove', (event) => {
    if (!isMouseDown) return;

    const touch = event.touches[0];
    const deltaMove = {
        x: previousMousePosition.x - touch.clientX,
        y: previousMousePosition.y - touch.clientY,
    };

    if (model) {
        model.rotation.y += deltaMove.x * 0.01;
        model.rotation.x -= deltaMove.y * 0.01;
    }

    previousMousePosition = {
        x: touch.clientX,
        y: touch.clientY,
    };

    clearTimeout(idleTimeout);
    idleTimeout = setTimeout(() => {
        animationActive = true;
    }, idleTime);

    event.preventDefault();
});

canvas.addEventListener('touchend', () => {
    isMouseDown = false;
});
