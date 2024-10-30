from flask import Flask, redirect, url_for, render_template, request
from flask_caching import Cache
import random
import re
from google import generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config['UPLOAD_FOLDER'] = '/uploads'

# Variaveis #
quantidade_itens_recomendados: int = 45

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
        'tags': ['decoracao', 'jardim'],
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
        'dimensoes': '30cm x 20cm x 15cm',
        'estoque': 5,
        'tags': ['armazenamento', 'organizacao'],
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
        'tags': ['organizacao'],
        'descricao': 'Dispenser prático para armazenar e organizar pilhas AA e AAA.'
    },
    {
        'nome': 'Funil',
        'imagem': 'img/produtos/funil.png',
        'preco': '20.00',
        'favorito': False,
        'peso': '80g',
        'material': 'PLA',
        'densidade': '15%',
        'dimensoes': '15cm x 10cm x 10cm',
        'estoque': 20,
        'tags': [],
        'descricao': 'Funil de plástico resistente, perfeito para transferência de líquidos na cozinha.'
    },
    {
        'nome': 'Garfo',
        'imagem': 'img/produtos/garfo.png',
        'preco': '15.00',
        'favorito': True,
        'peso': '30g',
        'material': 'PLA',
        'densidade': '10%',
        'dimensoes': '18cm x 3cm x 1cm',
        'estoque': 50,
        'tags': [],
        'descricao': 'Garfo impresso em 3D, ideal para uso diário ou em piqueniques.'
    },
    {
        'nome': 'Mesas e cadeiras',
        'imagem': 'img/produtos/mesas_cadeiras.png',
        'preco': '100.00',
        'favorito': False,
        'peso': '1200g',
        'material': 'ABS',
        'densidade': '40%',
        'dimensoes': '60cm x 60cm x 80cm',
        'estoque': 2,
        'tags': ['decoracao'],
        'descricao': 'Conjunto de mesa e cadeiras, perfeito para decoração de interiores e espaços compactos.'
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
        'tags': ['organizacao', 'escritorio'],
        'descricao': 'Porta lápis moderno para organizar sua mesa de escritório com estilo.'
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
        'tags': ['decoracao', 'brinquedos'],
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
        'tags': ['decoracao', 'brinquedos'],
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
        'tags': ['decoracao', 'brinquedos'],
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
        'tags': ['decoracao', 'brinquedos'],
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
        'tags': ['decoracao', 'brinquedos'],
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
        'tags': ['escritorio'],
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
        'tags': ['brinquedos', 'decoracao'],
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
        'tags': ['brinquedos', 'decoracao'],
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
    f"Agora, a mensagem do usuário: ")


@app.route('/')
@cache.cached(timeout=60)
def index():
    return render_template('index.html', produtos=lista_produtos)


@app.route('/produtos', methods=["GET", "POST"])
@cache.cached(timeout=60)
def produtos():
    if request.method == "POST":
        nome_produto = request.form.get('produto')
        for item in lista_produtos:
            if item['nome'] == nome_produto:
                item['favorito'] = True
                return redirect('carrinho')
    return render_template('produtos.html', produtos=lista_produtos)


@app.route('/produtos/<nome_produto>', methods=["GET"])
@cache.cached(timeout=60)
def produto_especifico(nome_produto):
    if request.method == "GET":
        for item in lista_produtos:
            if item['nome'] == nome_produto:
                return render_template('produto.html', produto=item)


@app.route('/carrinho', methods=["GET", "POST"])
@cache.cached(timeout=60)
def carrinho():
    recomendacoes = []
    lista_carrinho = []

    if request.method == "POST":
        nome_produto = request.form.get('produto')
        for item in lista_produtos:
            if item['nome'] == nome_produto:
                item['favorito'] = False
                return redirect('carrinho')

    for randon in range(quantidade_itens_recomendados):
        recomendacoes.append(random.choice(lista_produtos))

    for item in lista_produtos:
        if item['favorito']:
            lista_carrinho.append(item)

    if not lista_carrinho:
        return render_template('carrinho_vazio.html', recomendacoes=recomendacoes)

    return render_template('carrinho.html', carrinho=lista_carrinho, valorTotal=valor_total(lista_carrinho))


@app.route('/produtos-filtrados')
def produtos_filtrados():
    filtro_nome = request.args.get('filtro-nome', '').strip().lower()
    filtro_tag = request.args.get('tag', '').strip().lower()
    lista_filtrada = []

    # Quando ambos os filtros estão vazios, exibe todos os produtos
    if not filtro_nome and not filtro_tag:
        lista_filtrada = lista_produtos
    else:
        # Filtragem de acordo com os parâmetros inseridos
        for produto in lista_produtos:
            nome_corresponde = re.search(filtro_nome, produto.get('nome', '').lower()) if filtro_nome else True
            tag_corresponde = filtro_tag in (produto.get('tags') or []) if filtro_tag else True

            # Adiciona o produto se corresponder aos critérios ativos
            if nome_corresponde and tag_corresponde:
                lista_filtrada.append(produto)

    # Renderiza a mensagem se nenhum produto foi encontrado
    if not lista_filtrada:
        return render_template('produtos.html', produtos=[], mensagem="Nenhum produto encontrado")

    return render_template('produtos.html', produtos=lista_filtrada)


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
def chatbot():
    return render_template('chatbot.html')


@app.route('/search')
def search():
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
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


@app.route('/criar')
@cache.cached(timeout=60)
def criar():
    return render_template('criar.html')


def valor_total(lista):
    total = 0
    for produto in lista:
        total += float(produto['preco'])
    return f"{total:.2f}"


if __name__ == '__main__':
    app.run(debug=True)
