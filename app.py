from flask import Flask, redirect
from banco.classe_banco import Banco
from rotas.routes_autor import bp_autor
from rotas.routes_genero import bp_genero
from rotas.routes_proposta import bp_proposta
from rotas.routes_titulo import bp_titulo
from rotas.routes_usuario import bp_usuario

Banco().inicializar_Banco()

app = Flask(__name__, static_folder="interface", static_url_path="")
app.secret_key = "e-scamboo-chave-secreta"

app.register_blueprint(bp_usuario)
app.register_blueprint(bp_autor)
app.register_blueprint(bp_genero)
app.register_blueprint(bp_titulo)
app.register_blueprint(bp_proposta)

@app.route("/")
def inicio():
    return redirect("/livros.html")

if(__name__ == "__main__"):
    app.run()
