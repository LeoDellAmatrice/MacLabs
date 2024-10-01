from flask import Flask, redirect, url_for, render_template, request
import os
app = Flask(__name__)


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
    return render_template('produtos.html')


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

