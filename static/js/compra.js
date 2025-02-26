let produtosLocalStorage = window.localStorage.getItem("produtos");

let totalT = 0

function criar_item() {


    if (produtosLocalStorage != null) {

        produtosLocalStorage = JSON.parse(produtosLocalStorage);

        for (let i = 0; i < produtosLocalStorage.length; i++) {
            let produto = produtosLocalStorage[i]

            totalT += produto.preco * produto.quantidade;

            const div_checkot = document.createElement('div')
            div_checkot.classList.add('checkout-item')

            const img = document.createElement("img");
            img.src = `static/${produto.imagem}`;
            div_checkot.appendChild(img);

            const div_info = document.createElement('div')
            div_checkot.classList.add('item-info')
            div_checkot.appendChild(div_info);

            const nome = document.createElement('h3')
            nome.textContent = produto.nome
            const quant = document.createElement('p')
            quant.textContent = `Quantidade: ${produto.quantidade}`

            div_info.appendChild(nome)
            div_info.appendChild(quant)

            if (produto.quantidade !== 1){
                const preco = document.createElement('p')
                preco.textContent = `Preço unitário R$: ${produto.preco}`
                const texttotal = document.createElement('p')
                texttotal.textContent = `Total: R$: ${Number((produto.preco) * (produto.quantidade)).toFixed(2)}`
                div_info.appendChild(preco)
                div_info.appendChild(texttotal)
            } else {
                const preco = document.createElement('p')
                preco.textContent = `Total R$: ${produto.preco}`
                div_info.appendChild(preco)
            }


            const list_checkout = document.getElementById('checkout-list')

            list_checkout.appendChild(div_checkot);

        }

    }
    document.getElementById('subtotal').textContent = `Total: R$ ${Number(totalT).toFixed(2)}`
    document.getElementById('total').textContent = `Total + Frete: R$ ${Number(totalT+15).toFixed(2)}`
}

criar_item()