function login_menu() {
    const menu = document.getElementById('login-menu');
    const overlay = document.getElementById('overlay');
    const isOpen = menu.classList.toggle('open'); // Alterna a classe 'open'

    if (isOpen) {
        // Exibe o overlay e bloqueia a rolagem
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    } else {
        // Oculta o overlay e restaura a rolagem
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Fecha o menu e restaura a rolagem ao clicar no overlay
document.getElementById('overlay').addEventListener('click', () => {
    const menu = document.getElementById('login-menu');
    const overlay = document.getElementById('overlay');
    menu.classList.remove('open');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
});


const usuarioLocalStorage = window.localStorage.getItem("usuario");
const div_usuario_logado = document.getElementById("nav-buttons-logado");
const div_usuario_nao_logado = document.getElementById("nav-buttons");
const call = document.getElementById("call-to-action");

if (usuarioLocalStorage != null) {
    const usuario_logado = document.getElementById("usuario-logado");
    const usuario_logado_menu = document.getElementById("usuario-logado-menu");
    usuario_logado.textContent = usuarioLocalStorage
    usuario_logado_menu.textContent = "Usuario: " + usuarioLocalStorage;
    div_usuario_logado.style.display = "flex";
    div_usuario_nao_logado.style.display = "none";
    call.style.display = "none";
} else {
    div_usuario_nao_logado.style.display = "flex";
    div_usuario_logado.style.display = "none";
    call.style.display = "block";
}

function desconectar() {
    window.localStorage.removeItem("usuario");
    window.location.href = "/";
}