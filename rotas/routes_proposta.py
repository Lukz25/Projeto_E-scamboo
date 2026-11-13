from flask import Blueprint, request, jsonify
from arquivoClasses.classes import Proposta, Titulo
from rotas.routes_usuario import usuario_logado

bp_proposta = Blueprint("/proposta/", "__name__", url_prefix= "/proposta")

def proposta_para_json(proposta: Proposta) -> dict:
    return {
        "id": proposta.id,
        "interessado": proposta.interessado.get_email(),
        "titulo_desejado": proposta.titulo_desejado.nome,
        "dono": proposta.titulo_desejado.usuario.get_email(),
        "titulos_oferecidos": [titulo.nome for titulo in proposta.titulos_oferecidos],
        "observacao": proposta.observacao,
        "data_criacao": proposta.data_criacao.isoformat(),
        "situacao": proposta.situacao,
    }

@bp_proposta.route("/", methods=['GET'])
def listar():
    return jsonify([proposta_para_json(proposta) for proposta in Proposta.listar()]), 200

@bp_proposta.route("/<int:id>", methods=['GET'])
def buscar(id):
    proposta = Proposta.buscar(id)
    if proposta is None:
        return jsonify({'erro': 'Proposta não encontrada.'}), 404
    return jsonify(proposta_para_json(proposta)), 200

@bp_proposta.route("/", methods=['POST'])
def fazer_proposta():
    usuario = usuario_logado()
    if usuario is None:
        return jsonify({'erro': 'Faça login primeiro.'}), 401

    corpo = request.get_json()
    titulo_desejado = Titulo.buscar(corpo.get('titulo_desejado', 0))
    titulos_oferecidos = [Titulo.buscar(id) for id in corpo.get('titulos_oferecidos', [])]
    if titulo_desejado is None or None in titulos_oferecidos:
        return jsonify({'erro': 'Título não encontrado.'}), 404

    try:
        proposta = usuario.fazer_proposta(titulo_desejado, titulos_oferecidos, corpo.get('observacao', ''))
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    proposta.salvar()
    return jsonify(proposta_para_json(proposta)), 201

@bp_proposta.route("/<int:id>/<acao>", methods=['POST'])
def responder(id, acao):
    usuario = usuario_logado()
    if usuario is None:
        return jsonify({'erro': 'Faça login primeiro.'}), 401
    proposta = Proposta.buscar(id)
    if proposta is None:
        return jsonify({'erro': 'Proposta não encontrada.'}), 404

    try:
        if acao == "aceitar":
            proposta.aceitar_proposta(usuario)
        elif acao == "recusar":
            proposta.recusar_proposta(usuario)
        elif acao == "cancelar":
            proposta.cancelar_proposta(usuario)
        else:
            return jsonify({'erro': 'Ação inválida.'}), 404
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400

    proposta.salvar()
    return jsonify(proposta_para_json(proposta)), 200
