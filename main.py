from flask import Flask, redirect, url_for, render_template, request
from google import generativeai as genai
from flask_caching import Cache
from dotenv import load_dotenv
from random import sample, choice
import re
import os

load_dotenv()
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config['UPLOAD_FOLDER'] = '/uploads'

# Variaveis #
quantidade_itens_recomendados: int = 8
produtos_por_pagina: int = 18  # Número de produtos por página

lista_produtos = [
    {
        'nome': 'Prato para vaso',
        'imagem': 'img/produtos/pote_flor.svg',
        'preco': '30.00',
        'favorito': False,
        'peso': '150g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '20cm x 20cm x 2cm',
        'estoque': 10,
        'tags': ['decoração', 'jardim'],
        'descricao': 'Prato para vaso de plantas, ideal para manter a água e evitar sujeira em sua casa.'
    },
    {
        'nome': 'Caixa empilhável',
        'imagem': 'img/produtos/caixa_empilhavel.svg',
        'preco': '50.00',
        'favorito': False,
        'peso': '400g',
        'material': 'PETG',
        'densidade': '30%',
        'dimensoes': '30cm x 30cm x 15cm',
        'estoque': 5,
        'tags': ['armazenamento', 'organização'],
        'descricao': 'Caixa empilhável resistente, ideal para organizar e armazenar objetos.'
    },
    {
        'nome': 'Dispenser de pilhas',
        'imagem': 'img/produtos/dispenser_pilha.png',
        'preco': '25.00',
        'favorito': False,
        'peso': '120g',
        'material': 'ABS',
        'densidade': '20%',
        'dimensoes': '10cm x 5cm x 5cm',
        'estoque': 15,
        'tags': ['organização'],
        'descricao': 'Dispenser prático para armazenar e organizar pilhas AA e AAA.'
    },
    {
        'nome': 'Porta lápis',
        'imagem': 'img/produtos/porta_lapis.png',
        'preco': '18.00',
        'favorito': False,
        'peso': '70g',
        'material': 'PETG',
        'densidade': '20%',
        'dimensoes': '10cm x 10cm x 12cm',
        'estoque': 25,
        'tags': ['organização', 'escritório'],
        'descricao': 'Porta lápis moderno para organizar sua mesa de escritório com estilo.'
    },
    {
        'nome': 'Suporte para USBs',
        'imagem': 'img/produtos/usb_suporte.png',
        'preco': '22.00',
        'favorito': False,
        'peso': '100g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '4cm x 12cm x 4cm',
        'estoque': 10,
        'tags': ['escritório', 'organização'],
        'descricao': 'Suporte para USB e cartões de memoria, ideal para mantê-los protegidos.'
    },
    {
        'nome': 'Caixa com Divisorias',
        'imagem': 'img/produtos/caixa_divisoria.png',
        'preco': '34.00',
        'favorito': False,
        'peso': '220g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '10cm x 15cm x 6cm',
        'estoque': 10,
        'tags': ['organização', 'armazenamento'],
        'descricao': 'Caixa com divisorias para facilitar a separação de peças pequenas.'
    },
    {
        'nome': 'Shuriken',
        'imagem': 'img/produtos/shuriken.png',
        'preco': '10.00',
        'favorito': False,
        'peso': '50g',
        'material': 'PLA',
        'densidade': '25%',
        'dimensoes': '12cm x 12cm x 1cm',
        'estoque': 30,
        'tags': ['decoraçao', 'brinquedos'],
        'descricao': 'Shuriken decorativa, ideal para fãs de cultura oriental e artes marciais.'
    },
    {
        'nome': 'Elefante',
        'imagem': 'img/produtos/elefante.png',
        'preco': '40.00',
        'favorito': False,
        'peso': '200g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '15cm x 10cm x 10cm',
        'estoque': 8,
        'tags': ['decoração', 'brinquedos'],
        'descricao': 'Miniatura de elefante impresso em 3D, ótimo para decoração e colecionadores.'
    },
    {
        'nome': 'Sapo',
        'imagem': 'img/produtos/sapo.png',
        'preco': '35.00',
        'favorito': False,
        'peso': '150g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '10cm x 10cm x 8cm',
        'estoque': 10,
        'tags': ['decoração', 'brinquedos'],
        'descricao': 'Sapo decorativo impresso em 3D, ideal para coleções ou decoração temática.'
    },
    {
        'nome': 'Gato',
        'imagem': 'img/produtos/gato.png',
        'preco': '38.00',
        'favorito': False,
        'peso': '170g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '12cm x 8cm x 10cm',
        'estoque': 12,
        'tags': ['decoração', 'brinquedos'],
        'descricao': 'Figura de gato impresso em 3D, um toque especial para sua decoração.'
    },
    {
        'nome': 'Chave de boca ajustável',
        'imagem': 'img/produtos/chave_de_boca_ajustavel.png',
        'preco': '22.00',
        'favorito': True,
        'peso': '100g',
        'material': 'ABS',
        'densidade': '25%',
        'dimensoes': '20cm x 5cm x 2cm',
        'estoque': 18,
        'tags': ['ferramentas'],
        'descricao': 'Chave de boca ajustável funcional, ideal para pequenos reparos.'
    },
    {
        'nome': 'Tubarão articulado',
        'imagem': 'img/produtos/tubarao_articulado.png',
        'preco': '50.00',
        'favorito': False,
        'peso': '300g',
        'material': 'PETG',
        'densidade': '20%',
        'dimensoes': '30cm x 10cm x 5cm',
        'estoque': 7,
        'tags': ['decoração', 'brinquedos'],
        'descricao': 'Modelo de tubarão articulado, perfeito para decoração e coleções.'
    },
    {
        'nome': 'Mini catapulta',
        'imagem': 'img/produtos/mini_catapulta.png',
        'preco': '45.00',
        'favorito': False,
        'peso': '250g',
        'material': 'PLA',
        'densidade': '30%',
        'dimensoes': '15cm x 10cm x 8cm',
        'estoque': 6,
        'tags': ['brinquedos'],
        'descricao': 'Mini catapulta funcional, excelente para entusiastas de engenharia.'
    },
    {
        'nome': 'Suporte para celular',
        'imagem': 'img/produtos/suporte_para_celular.png',
        'preco': '25.00',
        'favorito': False,
        'peso': '80g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '10cm x 8cm x 5cm',
        'estoque': 20,
        'tags': ['escritório'],
        'descricao': 'Suporte para celular prático e moderno, ideal para mesas de escritório.'
    },
    {
        'nome': 'Coelho',
        'imagem': 'img/produtos/coelho.png',
        'preco': '32.00',
        'favorito': False,
        'peso': '180g',
        'material': 'PLA',
        'densidade': '20%',
        'dimensoes': '15cm x 8cm x 10cm',
        'estoque': 10,
        'tags': ['brinquedos', 'decoração'],
        'descricao': 'Figura decorativa de coelho, perfeita para decorações temáticas e coleções.'
    },
    {
        'nome': 'Foguete',
        'imagem': 'img/produtos/foguete.png',
        'preco': '55.00',
        'favorito': False,
        'peso': '350g',
        'material': 'ABS',
        'densidade': '25%',
        'dimensoes': '25cm x 10cm x 10cm',
        'estoque': 4,
        'tags': ['brinquedos', 'decoraçãoe'],
        'descricao': 'Modelo de foguete impresso em 3D, ideal para decoração de temas espaciais.'
    },
    {
        'nome': 'Anel de gato',
        'imagem': 'img/produtos/anel_de_gato.png',
        'preco': '12.00',
        'favorito': False,
        'peso': '10g',
        'material': 'PLA',
        'densidade': '15%',
        'dimensoes': '2cm x 2cm x 0.5cm',
        'estoque': 50,
        'tags': ['brinquedos'],
        'descricao': 'Anel estiloso em formato de gato, ideal para amantes de felinos.'
    }
]

# for i in range(199):
#     lista_produtos.append(choice(lista_produtos))

context = (
    f"Você é o chatbot da MacLabs, especializado em guiar usuários no site e responder perguntas sobre nossos produtos e serviços de impressão 3D."
    f"Caso o usuário queira saber mais sobre a empresa, ofereça uma resposta sucinta e sugira que visite a aba Sobre do site para mais detalhes."
    f"Nosso catálogo inclui: {lista_produtos}. Os principais setores do site são:"
    f"Produtos: onde todos os itens disponíveis estão listados."
    f"SandBox: um ambiente interativo para criar produtos personalizados."
    f"Contato: uma área ao final de cada página para suporte direto."
    f"Sobre: uma seção dedicada à história, valores e missão da MacLabs."
    f"A missão da MacLabs é 'Incentivar a criatividade e inovação dos nossos clientes, transformando ideias em realidade'."
    f" Nossa visão é 'Ser uma empresa que oferece aos clientes a chance de mudar o mundo'."
    f" Valorizamos 'Criatividade, inovação, ética, sustentabilidade, qualidade e disciplina.'"
    f"Caso você diga para o usuário visitar uma pagina do site, escreva a tag do HTML <a></a> com href para a pagina que se referencia com todas as letras minusculas(produtos, sobre, exibir_carrinho, #contato)"
    f"Agora, a mensagem do usuário: ")


@app.route('/')
@cache.cached(timeout=60)
def index():
    return render_template('index.html', produtos=lista_produtos)


@app.route('/compra-realizada')
def agradecimento():
    return render_template('agradecimento.html')


@app.route('/produtos', methods=["GET"])
def produtos():
    pagina = int(request.args.get('pagina', 1))
    filtro_nome = request.args.get('filtro-nome', '').strip().lower()
    filtro_tag = request.args.getlist('tag')

    produtos_filtrados = lista_produtos  # Inicialmente, todos os produtos
    if filtro_nome or filtro_tag:
        produtos_filtrados = [
            produto for produto in lista_produtos
            if (filtro_nome in produto['nome'].lower() if filtro_nome else True) and
               (any(tag in produto.get('tags', []) for tag in filtro_tag) if filtro_tag else True)
        ]

    # Paginação
    total_paginas = (len(produtos_filtrados) + produtos_por_pagina - 1) // produtos_por_pagina
    inicio = (pagina - 1) * produtos_por_pagina
    fim = inicio + produtos_por_pagina

    produtos_pagina = produtos_filtrados[inicio:fim]

    # Construir URLs para navegação com os filtros aplicados
    query_filtros = f"filtro-nome={filtro_nome}&" + "&".join([f"tag={tag}" for tag in filtro_tag])
    proxima_pagina = f"/produtos?{query_filtros}&pagina={pagina + 1}" if fim < len(produtos_filtrados) else None
    pagina_anterior = f"/produtos?{query_filtros}&pagina={pagina - 1}" if inicio > 0 else None

    return render_template(
        'produtos.html',
        produtos=produtos_pagina,
        total_paginas=total_paginas,
        pagina=pagina,
        proxima_pagina=proxima_pagina,
        pagina_anterior=pagina_anterior,
        filtro_nome=filtro_nome,
        filtro_tag=filtro_tag
    )


@app.route('/produtos/<nome_produto>', methods=["GET"])
def produto_especifico(nome_produto):
    if request.method == "GET":
        for item in lista_produtos:
            if item['nome'] == nome_produto:
                return render_template('produto.html', produto=item)


@app.route('/exibir_carrinho')
def exibir_carrinho():
    recomenda_lista = sample(lista_produtos, k=quantidade_itens_recomendados)
    return render_template('carrinho.html', recomendacoes=recomenda_lista)


@app.route("/login", methods=["GET", "POST"])
@cache.cached(timeout=60)
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario == "maclabs":
            if senha == "1234":
                return redirect(url_for('upload'))

        return render_template("login.html")


@app.route('/inscricao')
@cache.cached(timeout=60)
def inscricao():
    return render_template('inscricao.html')


@app.route('/chatbot')
@cache.cached(timeout=60)
def chatbot():
    return render_template('chatbot.html')


@app.route('/search')
def search():
    model = genai.GenerativeModel('gemini-1.5-flash')
    genai.configure(api_key=os.getenv('API'))
    prompt = request.args.get('prompt')
    input_ia = f'{context}: {prompt}'
    output = model.generate_content(input_ia)
    return {'message': output.text}


@app.route('/upload', methods=["GET", "POST"])
@cache.cached(timeout=60)
def upload():
    if request.method == "GET":
        return render_template('upload.html')
    elif request.method == "POST":
        file = request.files["file"]
        caminho = app.config["UPLOAD_FOLDER"] + "/" + file.filename
        file.save(caminho)
        return render_template("produtos.html")


@app.route('/sobre')
@cache.cached(timeout=60)
def sobre():
    return render_template('sobre.html')


@app.route('/sandbox')
@cache.cached(timeout=60)
def sandbox():
    return render_template('sandbox.html')


@app.route('/comprar')
def comprar():
    return render_template('compra.html')


if __name__ == '__main__':
    app.run(debug=True)
