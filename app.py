from flask import Flask
from rotas.routes_autor import bp_autor
from rotas.routes_genero import bp_genero
from rotas.routes_proposta import bp_proposta
from rotas.routes_titulo import bp_titulo
from rotas.routes_usuario import bp_usuario

app = Flask(__name__)
app.secret_key = "e-scamboo-chave-secreta"

app.register_blueprint(bp_usuario)
app.register_blueprint(bp_autor)
app.register_blueprint(bp_genero)
app.register_blueprint(bp_titulo)
app.register_blueprint(bp_proposta)

if(__name__ == "__main__"):
    app.run()