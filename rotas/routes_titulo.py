from flask import Blueprint, request, jsonify
from arquivoClasses.classes import Titulo
from arquivoClasses.dados import dados

bp_titulo = Blueprint("/titulo/", "__name__", url_prefix= "/titulo")

def titulo_para_json(titulo: Titulo) -> dict:
    return {
        "id": titulo.id,
        "nome": titulo.nome,
        "dono": titulo.usuario.get_email(),
        "autores": [autor.nome for autor in titulo.autores],
        "generos": [genero.nome for genero in titulo.generos],
        "data_lancamento": titulo.data_lancamento,
        "estado_conservacao": titulo.estado_conservacao,
        "descricao": titulo.descricao,
    }

@bp_titulo.route("/", methods=['GET'])
def listar():
    titulos = list(dados.titulos.values())

    autor = dados.autores.get(request.args.get('autor', type=int))
    if autor is not None:
        titulos = [titulo for titulo in titulos if titulo.possui_autor(autor)]

    genero = dados.generos.get(request.args.get('genero', type=int))
    if genero is not None:
        titulos = [titulo for titulo in titulos if titulo.possui_genero(genero)]

    return jsonify([titulo_para_json(titulo) for titulo in titulos]), 200

@bp_titulo.route("/<int:id>", methods=['GET'])
def buscar(id):
    titulo = dados.titulos.get(id)
    if titulo is None:
        return jsonify({'erro': 'Título não encontrado.'}), 404
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/", methods=['POST'])
def cadastrar():
    corpo = request.get_json()
    nome = corpo.get('nome')
    usuario = dados.usuarios.get(corpo.get('email'))
    autores = [dados.autores.get(id) for id in corpo.get('autores', [])]
    generos = [dados.generos.get(id) for id in corpo.get('generos', [])]
    if not nome:
        return jsonify({'erro': 'Informe o nome do título.'}), 400
    if usuario is None:
        return jsonify({'erro': 'Usuário não encontrado.'}), 404
    if None in autores:
        return jsonify({'erro': 'Autor não encontrado.'}), 404
    if None in generos:
        return jsonify({'erro': 'Gênero não encontrado.'}), 404

    novo_id = max(dados.titulos, default=0) + 1
    titulo = Titulo(
        novo_id,
        nome,
        usuario,
        autores,
        generos,
        corpo.get('data_lancamento', ''),
        corpo.get('estado_conservacao', ''),
        corpo.get('descricao', ''),
    )
    dados.titulos[novo_id] = titulo
    return jsonify(titulo_para_json(titulo)), 201

@bp_titulo.route("/<int:id>", methods=['PUT'])
def atualizar(id):
    titulo = dados.titulos.get(id)
    if titulo is None:
        return jsonify({'erro': 'Título não encontrado.'}), 404

    corpo = request.get_json()
    titulo.nome = corpo.get('nome', titulo.nome)
    titulo.data_lancamento = corpo.get('data_lancamento', titulo.data_lancamento)
    titulo.estado_conservacao = corpo.get('estado_conservacao', titulo.estado_conservacao)
    titulo.descricao = corpo.get('descricao', titulo.descricao)
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>", methods=['DELETE'])
def remover(id):
    titulo = dados.titulos.get(id)
    if titulo is None:
        return jsonify({'erro': 'Título não encontrado.'}), 404
    for proposta in dados.propostas:
        if proposta.esta_pendente() and (titulo is proposta.titulo_desejado or titulo in proposta.titulos_oferecidos):
            return jsonify({'erro': 'Título está em uma proposta pendente.'}), 400

    for autor in list(titulo.autores):
        titulo.remover_autor(autor)
    titulo.usuario.remover_titulo_biblioteca(titulo)
    for usuario in dados.usuarios.values():
        usuario.desfavoritar_titulo(titulo)
    del dados.titulos[id]
    return jsonify({'mensagem': 'Título removido.'}), 200

@bp_titulo.route("/<int:id>/autores/<int:autor_id>", methods=['POST'])
def adicionar_autor(id, autor_id):
    titulo = dados.titulos.get(id)
    autor = dados.autores.get(autor_id)
    if titulo is None or autor is None:
        return jsonify({'erro': 'Título ou autor não encontrado.'}), 404

    titulo.adicionar_autor(autor)
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>/autores/<int:autor_id>", methods=['DELETE'])
def remover_autor(id, autor_id):
    titulo = dados.titulos.get(id)
    autor = dados.autores.get(autor_id)
    if titulo is None or autor is None:
        return jsonify({'erro': 'Título ou autor não encontrado.'}), 404

    titulo.remover_autor(autor)
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>/generos/<int:genero_id>", methods=['POST'])
def adicionar_genero(id, genero_id):
    titulo = dados.titulos.get(id)
    genero = dados.generos.get(genero_id)
    if titulo is None or genero is None:
        return jsonify({'erro': 'Título ou gênero não encontrado.'}), 404

    titulo.adicionar_genero(genero)
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>/generos/<int:genero_id>", methods=['DELETE'])
def remover_genero(id, genero_id):
    titulo = dados.titulos.get(id)
    genero = dados.generos.get(genero_id)
    if titulo is None or genero is None:
        return jsonify({'erro': 'Título ou gênero não encontrado.'}), 404

    titulo.remover_genero(genero)
    return jsonify(titulo_para_json(titulo)), 200
