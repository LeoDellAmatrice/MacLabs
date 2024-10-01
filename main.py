from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/criar')
def criar():
    return render_template('criar.html')

@app.route('/produtos')
def produtos():
    return render_template('produtos.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/inscricao')
def inscricao():
    return render_template('inscricao.html')


if __name__ == '__main__':
    app.run(debug=True)

