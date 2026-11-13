from flask import Blueprint, request, jsonify
from arquivoClasses.classes import Autor, Genero, Titulo, Usuario

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
    titulos = Titulo.listar()

    autor_id = request.args.get('autor', type=int)
    if autor_id is not None:
        autor = Autor.buscar(autor_id)
        titulos = [titulo for titulo in titulos if autor is not None and titulo.possui_autor(autor)]

    genero_id = request.args.get('genero', type=int)
    if genero_id is not None:
        genero = Genero.buscar(genero_id)
        titulos = [titulo for titulo in titulos if genero is not None and titulo.possui_genero(genero)]

    return jsonify([titulo_para_json(titulo) for titulo in titulos]), 200

@bp_titulo.route("/<int:id>", methods=['GET'])
def buscar(id):
    titulo = Titulo.buscar(id)
    if titulo is None:
        return jsonify({'erro': 'Título não encontrado.'}), 404
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/", methods=['POST'])
def cadastrar():
    corpo = request.get_json()
    nome = corpo.get('nome')
    if not nome:
        return jsonify({'erro': 'Informe o nome do título.'}), 400
    usuario = Usuario.buscar(corpo.get('email', ''))
    if usuario is None:
        return jsonify({'erro': 'Usuário não encontrado.'}), 404
    autores = [Autor.buscar(id) for id in corpo.get('autores', [])]
    if None in autores:
        return jsonify({'erro': 'Autor não encontrado.'}), 404
    generos = [Genero.buscar(id) for id in corpo.get('generos', [])]
    if None in generos:
        return jsonify({'erro': 'Gênero não encontrado.'}), 404

    titulo = Titulo(
        None,
        nome,
        usuario,
        autores,
        generos,
        corpo.get('data_lancamento', ''),
        corpo.get('estado_conservacao', ''),
        corpo.get('descricao', ''),
    )
    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 201

@bp_titulo.route("/<int:id>", methods=['PUT'])
def atualizar(id):
    titulo = Titulo.buscar(id)
    if titulo is None:
        return jsonify({'erro': 'Título não encontrado.'}), 404

    corpo = request.get_json()
    titulo.nome = corpo.get('nome', titulo.nome)
    titulo.data_lancamento = corpo.get('data_lancamento', titulo.data_lancamento)
    titulo.estado_conservacao = corpo.get('estado_conservacao', titulo.estado_conservacao)
    titulo.descricao = corpo.get('descricao', titulo.descricao)
    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>", methods=['DELETE'])
def remover(id):
    titulo = Titulo.buscar(id)
    if titulo is None:
        return jsonify({'erro': 'Título não encontrado.'}), 404

    try:
        titulo.remover()
    except ValueError as erro:
        return jsonify({'erro': str(erro)}), 400
    return jsonify({'mensagem': 'Título removido.'}), 200

@bp_titulo.route("/<int:id>/autores/<int:autor_id>", methods=['POST'])
def adicionar_autor(id, autor_id):
    titulo = Titulo.buscar(id)
    autor = Autor.buscar(autor_id)
    if titulo is None or autor is None:
        return jsonify({'erro': 'Título ou autor não encontrado.'}), 404

    titulo.adicionar_autor(autor)
    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>/autores/<int:autor_id>", methods=['DELETE'])
def remover_autor(id, autor_id):
    titulo = Titulo.buscar(id)
    autor = Autor.buscar(autor_id)
    if titulo is None or autor is None:
        return jsonify({'erro': 'Título ou autor não encontrado.'}), 404

    titulo.remover_autor(autor)
    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>/generos/<int:genero_id>", methods=['POST'])
def adicionar_genero(id, genero_id):
    titulo = Titulo.buscar(id)
    genero = Genero.buscar(genero_id)
    if titulo is None or genero is None:
        return jsonify({'erro': 'Título ou gênero não encontrado.'}), 404

    titulo.adicionar_genero(genero)
    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 200

@bp_titulo.route("/<int:id>/generos/<int:genero_id>", methods=['DELETE'])
def remover_genero(id, genero_id):
    titulo = Titulo.buscar(id)
    genero = Genero.buscar(genero_id)
    if titulo is None or genero is None:
        return jsonify({'erro': 'Título ou gênero não encontrado.'}), 404

    titulo.remover_genero(genero)
    titulo.salvar()
    return jsonify(titulo_para_json(titulo)), 200
