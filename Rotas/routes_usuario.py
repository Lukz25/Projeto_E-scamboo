from flask import Blueprint, request, jsonify, session
from arquivoClasses.classes import Usuario

bp_usuario = Blueprint("/usuario/", "__name__", url_prefix= "/usuario")

@bp_usuario.route("/Logar", methods=['POST'])
def Logar():
    dados = request.get_json()
    email = dados['email']
    senha = dados['senha']

    if(email == "tigrinho@hotmail.com.es" and senha == "2444666668888888"):
        session['usuario'] = email
        return jsonify({'situacao':True}), 200

    return jsonify({'situacao':False}), 401


