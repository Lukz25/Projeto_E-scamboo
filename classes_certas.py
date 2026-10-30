
from datetime import datetime


class Autor:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome
        self.obras: list[Titulo] = []


class Genero:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome


class Titulo:
    def __init__(
        self,
        id: int,
        nome: str,
        autores: list[Autor],
        generos: list[Genero],
        data_lancamento: str,
    ):
        self.id = id
        self.nome = nome
        self.autores = autores
        self.generos = generos
        self.data_lancamento = data_lancamento


class Usuario:
    def __init__(self, nome: str, email: str, telefone: str, endereco: str):
        self.nome = nome
        self.__email = email
        self.telefone = telefone
        self.endereco = endereco
        self.biblioteca: list[Titulo] = []
        self.favoritos: list[Titulo] = []


class Proposta:
    def __init__(
        self,
        anunciante: Usuario,
        titulos_propostos: list[Titulo],
        titulos_requeridos: list[Titulo],
        data_publicacao: datetime,
    ):
        self.anunciante = anunciante
        self.titulos_propostos = titulos_propostos
        self.titulos_requeridos = titulos_requeridos
        self.data_publicacao = data_publicacao
        self.interessados: list[Usuario] = []
        self.status = "aberta"
