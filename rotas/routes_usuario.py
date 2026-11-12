from flask import Blueprint, request, jsonify, session
from arquivoClasses.classes import Usuario
from arquivoClasses.dados import dados

bp_usuario = Blueprint("/usuario/", "__name__", url_prefix= "/usuario")

@bp_usuario.route("/Logar", methods=['POST'])
def Logar():
    corpo = request.get_json()
    email = corpo.get('email')
    senha = corpo.get('senha')
    if not email or not senha:
        return jsonify({'erro': 'Informe o e-mail e a senha.'}), 400

    usuario = dados.usuarios.get(email)
    if usuario is None or not usuario.verificar_senha(senha):
        return jsonify({'situacao':False}), 401

    session['usuario'] = email
    return jsonify({'situacao':True}), 200


