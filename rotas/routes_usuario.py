from flask import Blueprint, request, jsonify, session
from arquivoClasses.classes import Titulo, Usuario

bp_usuario = Blueprint("/usuario/", "__name__", url_prefix= "/usuario")

def usuario_logado() -> Usuario | None:
    email = session.get('usuario')
    if email is None:
        return None
    return Usuario.buscar(email)

def usuario_para_json(usuario: Usuario) -> dict:
    return {
        "email": usuario.get_email(),
        "nome": usuario.nome,
        "telefone": usuario.telefone,
        "cep": usuario.cep,
        "biblioteca": [titulo.nome for titulo in usuario.biblioteca],
        "favoritos": [titulo.nome for titulo in usuario.favoritos],
    }

@bp_usuario.route("/Logar", methods=['POST'])
def Logar():
    corpo = request.get_json()
    email = corpo.get('email')
    senha = corpo.get('senha')
    if not email or not senha:
        return jsonify({'erro': 'Informe o e-mail e a senha.'}), 400

    usuario = Usuario.buscar(email)
    if usuario is None or not usuario.verificar_senha(senha):
        return jsonify({'situacao':False}), 401

    session['usuario'] = email
    return jsonify({'situacao':True}), 200

@bp_usuario.route("/Deslogar", methods=['POST'])
def Deslogar():
    session.pop('usuario', None)
    return jsonify({'situacao':True}), 200

@bp_usuario.route("/", methods=['GET'])
def listar():
    return jsonify([usuario_para_json(usuario) for usuario in Usuario.listar()]), 200

@bp_usuario.route("/<email>", methods=['GET'])
def buscar(email):
    usuario = Usuario.buscar(email)
    if usuario is None:
        return jsonify({'erro': 'Usuário não encontrado.'}), 404
    return jsonify(usuario_para_json(usuario)), 200

@bp_usuario.route("/", methods=['POST'])
def cadastrar():
    corpo = request.get_json()
    nome = corpo.get('nome')
    email = corpo.get('email')
    senha = corpo.get('senha')
    if not nome or not email or not senha:
        return jsonify({'erro': 'Informe nome, e-mail e senha.'}), 400
    if Usuario.email_cadastrado(email):
        return jsonify({'erro': 'E-mail já cadastrado.'}), 400

    try:
        usuario = Usuario(nome, email, Usuario.gerar_hash(senha), corpo.get('telefone', ''), corpo.get('cep', ''))
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    usuario.salvar()
    return jsonify(usuario_para_json(usuario)), 201

@bp_usuario.route("/", methods=['PUT'])
def atualizar():
    usuario = usuario_logado()
    if usuario is None:
        return jsonify({'erro': 'Faça login primeiro.'}), 401

    corpo = request.get_json()
    usuario.nome = corpo.get('nome', usuario.nome)
    usuario.telefone = corpo.get('telefone', usuario.telefone)
    usuario.cep = corpo.get('cep', usuario.cep)
    try:
        if 'senha' in corpo:
            usuario.alterar_senha(corpo['senha'])
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    usuario.salvar()
    return jsonify(usuario_para_json(usuario)), 200

@bp_usuario.route("/", methods=['DELETE'])
def remover():
    usuario = usuario_logado()
    if usuario is None:
        return jsonify({'erro': 'Faça login primeiro.'}), 401

    try:
        usuario.remover()
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    session.pop('usuario', None)
    return jsonify({'mensagem': 'Usuário removido.'}), 200

@bp_usuario.route("/favoritos/<int:titulo_id>", methods=['POST'])
def favoritar(titulo_id):
    usuario = usuario_logado()
    if usuario is None:
        return jsonify({'erro': 'Faça login primeiro.'}), 401
    titulo = Titulo.buscar(titulo_id)
    if titulo is None:
        return jsonify({'erro': 'Título não encontrado.'}), 404

    usuario.favoritar_titulo(titulo)
    usuario.salvar()
    return jsonify(usuario_para_json(usuario)), 200

@bp_usuario.route("/favoritos/<int:titulo_id>", methods=['DELETE'])
def desfavoritar(titulo_id):
    usuario = usuario_logado()
    if usuario is None:
        return jsonify({'erro': 'Faça login primeiro.'}), 401
    titulo = Titulo.buscar(titulo_id)
    if titulo is None:
        return jsonify({'erro': 'Título não encontrado.'}), 404

    usuario.desfavoritar_titulo(titulo)
    usuario.salvar()
    return jsonify(usuario_para_json(usuario)), 200
