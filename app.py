from flask import Flask
from Rotas.routes_autor import bp_autor
from Rotas.routes_genero import bp_genero
from Rotas.routes_proposta import bp_proposta
from Rotas.routes_titulo import bp_titulo
from Rotas.routes_usuario import bp_usuario

app = Flask(__name__)

app.register_blueprint(bp_usuario)
app.register_blueprint(bp_autor)
app.register_blueprint(bp_genero)
app.register_blueprint(bp_titulo)
app.register_blueprint(bp_proposta)

if(__name__ == "__main__"):
    app.run()