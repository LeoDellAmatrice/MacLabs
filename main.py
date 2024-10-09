from flask import Flask, redirect, url_for, render_template, request
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/uploads'


@app.route('/')
def index():
    return render_template('index.html')


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
    lista_produtos = [
        {'nome': 'Prato para vaso', 'preco': 'R$ 100,00', 'imagem': 'img/produtos/pote_flor.svg'},
        {'nome': 'Caixa empilhavel', 'preco': 'R$ 150,00', 'imagem': 'img/produtos/caixa_empilhavel.svg'},
        {'nome': 'Caixa com divisorias empilhavel', 'preco': 'R$ 200,00', 'imagem': 'img/produtos/caixa_divisoria.svg'},
        {'nome': 'Dispenser de pilhas AA e AAA', 'preco': 'R$ 100,00', 'imagem': 'img/produtos/dispenser_pilha.png'},
        {'nome': 'Funil', 'preco': 'R$ 100,00', 'imagem': 'img/produtos/funil.png'},
        {'nome': 'Garfo', 'preco': 'R$ 100,00', 'imagem': 'img/produtos/garfo.png'},
        {'nome': 'Mesas e cadeiras', 'preco': 'R$ 100,00', 'imagem': 'img/produtos/mesas_cadeiras.png'},
        {'nome': 'Porta lápis', 'preco': 'R$ 100,00', 'imagem': 'img/produtos/porta_lapis.png'},
        {'nome': 'Shuriken', 'preco': 'R$ 100,00', 'imagem': 'img/produtos/shuriken.png'},
        # Adicione mais produtos conforme necessário
    ]

    return render_template('produtos.html', produtos=lista_produtos)


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
