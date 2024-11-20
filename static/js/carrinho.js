let produtosLocalStorage = window.localStorage.getItem("produtos");

let total = 0;

function criar_item() {

    if (produtosLocalStorage != null) {

        produtosLocalStorage = JSON.parse(produtosLocalStorage);

        for (let i = 0; i < produtosLocalStorage.length; i++) {
            let produto = produtosLocalStorage[i]
            total += produto.preco * produto.quantidade;
            const divcarrinho_item = document.createElement("div");
            divcarrinho_item.classList.add("carrinho-item");
            const img = document.createElement("img");

            img.src = `static/${produto.imagem}`;

            divcarrinho_item.appendChild(img);

            const divitem_info = document.createElement("div");
            divitem_info.classList.add("item-info");
            const h3 = document.createElement("h3");
            h3.textContent = produto.nome;
            const p = document.createElement("p");
            p.textContent = "Preço: R$ " + produto.preco;
            const p_quanti = document.createElement("p");
            p_quanti.textContent = "Quantidade: " + produto.quantidade + " Unidades";

            divitem_info.appendChild(h3);
            divitem_info.appendChild(p);
            divitem_info.appendChild(p_quanti);

            divcarrinho_item.appendChild(divitem_info);

            const divitenscarrinho = document.getElementById('carrinho-itens')

            divitenscarrinho.appendChild(divcarrinho_item);

            const divacao = document.createElement('div');
            divacao.classList.add('item-acoes');
            const form = document.createElement('form');
            const remover_item = document.createElement('button');
            remover_item.classList.add('remover-item');
            remover_item.textContent = 'Remover';
            remover_item.onclick = remover_do_carrinho.bind(this, produto.nome);

            form.appendChild(remover_item);
            divacao.appendChild(form);

            divcarrinho_item.appendChild(divacao);

        }

        document.getElementById('total').textContent = `R$: ${Number(total).toFixed(2)}`

    } else {
        const div_total = document.getElementById('carrinho-total')
        const botao_comprar = document.getElementById('botao-finalizar-compra')
        div_total.style.display = 'none'
        botao_comprar.style.display = 'none'

        const mensagem = document.createElement('H4')
        mensagem.textContent = 'Não há nenhum produto no carrinho.'
        mensagem.style = 'text-align:center;'

        const div_carrinho = document.getElementById('carrinho-itens')
        div_carrinho.appendChild(mensagem)
    }

}
function remover_do_carrinho(nome){
    for (let i = 0; i < produtosLocalStorage.length; i++){
        if (produtosLocalStorage[i].nome === nome){
            produtosLocalStorage.splice(i, 1);
            window.localStorage.setItem("produtos", JSON.stringify(produtosLocalStorage));
            location.reload();
            break;
        }
    }
    console.log(produtosLocalStorage.length)
    if (produtosLocalStorage != null) {
        if (produtosLocalStorage.length < 1){
            localStorage.removeItem('produtos')
        }
    }
}

criar_item()