from flask import Blueprint, request, jsonify
from classes import Usuario

bp_usuario = Blueprint("/usuario/", "__name__", url_prefix= "/usuario")

@bp_usuario.route("/Logar", methods=['POST'])
def Logar():
    dados = request.get_json()
    email = dados['email']
    senha = dados['senha']

    return jsonify({'situacao':True}), 200


