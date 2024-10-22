from flask import Flask, redirect, url_for, render_template, request
import os
import re
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/uploads'

lista_produtos: [str, str] = [
        {'nome': 'Prato para vaso', 'imagem': 'img/produtos/pote_flor.svg'},
        {'nome': 'Caixa empilhavel', 'imagem': 'img/produtos/caixa_empilhavel.svg'},
        {'nome': 'Dispenser de pilhas AA e AAA', 'imagem': 'img/produtos/dispenser_pilha.png'},
        {'nome': 'Funil', 'imagem': 'img/produtos/funil.png'},
        {'nome': 'Garfo', 'imagem': 'img/produtos/garfo.png'},
        {'nome': 'Mesas e cadeiras', 'imagem': 'img/produtos/mesas_cadeiras.png'},
        {'nome': 'Porta lápis', 'imagem': 'img/produtos/porta_lapis.png'},
        {'nome': 'Shuriken', 'imagem': 'img/produtos/shuriken.png'},
        {'nome': 'Elefante', 'imagem': 'img/produtos/elefante.png'},
        {'nome': 'Sapo', 'imagem': 'img/produtos/sapo.png'},
        {'nome': 'Gato', 'imagem': 'img/produtos/gato.png'},
        {'nome': 'Chave de boca ajustável', 'imagem': 'img/produtos/chave_de_boca_ajustavel.png'},
        {'nome': 'Tubarão articulado', 'imagem': 'img/produtos/tubarao_articulado.png'},
        {'nome': 'Mini catapulta', 'imagem': 'img/produtos/mini_catapulta.png'},
        {'nome': 'Suporte para celular', 'imagem': 'img/produtos/suporte_para_celular.png'},
        {'nome': 'Coelho', 'imagem': 'img/produtos/coelho.png'},
        {'nome': 'Foguete', 'imagem': 'img/produtos/foguete.png'},
        {'nome': 'Anel de gato', 'imagem': 'img/produtos/anel_de_gato.png'}
        # Adicione mais produtos conforme necessário
    ]


@app.route('/')
def index():
    return render_template('index.html', produtos=lista_produtos)


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template('upload.html')
    elif request.method == "POST":
        file = request.files["file"]
        caminho = app.config["UPLOAD_FOLDER"] + "/" + file.filename
        file.save(caminho)
        return render_template("produtos.html")


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/criar')
def criar():
    return render_template('criar.html')


@app.route('/produtos')
def produtos():

    return render_template('produtos.html', produtos=lista_produtos)


@app.route('/produtos-filtrados')
def produtos_filtrados():
    filtro = request.args.get('filtro-nome')
    lista_filtrada = []
    for produto in lista_produtos:
        if re.search(filtro.lower(), produto.get('nome').lower()):
            lista_filtrada.append(produto)

    if not lista_filtrada:
        return render_template('produtos.html', produtos=[], mensagem="Nenhum produto encontrado")
    return render_template('produtos.html', produtos=lista_filtrada)


@app.route("/login", methods=["GET", "POST"])
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
def inscricao():
    return render_template('inscricao.html')


if __name__ == '__main__':
    app.run(debug=True)
