
from datetime import datetime


class Autor:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome
        self.obras: list[Titulo] = []
        
    def adicionar_obra(self, titulo: "Titulo") -> None:
        if titulo not in self.obras:
            self.obras.append(titulo)
        if self not in titulo.autores:
            titulo.autores.append(self)

    def remover_obra(self, titulo: "Titulo") -> None:
        if titulo in self.obras:
            self.obras.remove(titulo)
        if self in titulo.autores:
            titulo.autores.remove(self)

    def __repr__(self) -> str:
        return f"Autor(id={self.id}, nome={self.nome!r})"


class Genero:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome
    
    def __repr__(self) -> str:
        return f"Genero(id={self.id}, nome={self.nome!r})"


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
    
    def adicionar_autor(self, autor: Autor) -> None:
        if autor not in self.autores:
            self.autores.append(autor)
        if self not in autor.obras:
            autor.obras.append(self)

    def remover_autor(self, autor: Autor) -> None:
        if autor in self.autores:
            self.autores.remove(autor)
        if self in autor.obras:
            autor.obras.remove(self)

    def adicionar_genero(self, genero: Genero) -> None:
        if genero not in self.generos:
            self.generos.append(genero)

    def remover_genero(self, genero: Genero) -> None:
        if genero in self.generos:
            self.generos.remove(genero)

    def possui_autor(self, autor: Autor) -> bool:
        return autor in self.autores

    def possui_genero(self, genero: Genero) -> bool:
        return genero in self.generos

    def __repr__(self) -> str:
        return f"Titulo(id={self.id}, nome={self.nome!r})"


class Usuario:
    def __init__(self, nome: str, email: str, telefone: str, endereco: str):
        self.nome = nome
        self.__email = email
        self.telefone = telefone
        self.endereco = endereco
        self.biblioteca: list[Titulo] = []
        self.favoritos: list[Titulo] = []
        
    def get_email(self) -> str:
        return self.__email

    def set_email(self, novo_email: str) -> None:
        if "@" not in novo_email:
            raise ValueError("E-mail inválido.")
        self.__email = novo_email

    def adicionar_titulo_biblioteca(self, titulo: Titulo) -> None:
        if titulo in self.biblioteca:
            raise ValueError("Título já está na biblioteca.")
        self.biblioteca.append(titulo)

    def remover_titulo_biblioteca(self, titulo: Titulo) -> None:
        if titulo not in self.biblioteca:
            raise ValueError("Título não está na biblioteca.")
        self.biblioteca.remove(titulo)
        if titulo in self.favoritos:
            self.favoritos.remove(titulo)

    def possui_titulo(self, titulo: Titulo) -> bool:
        return titulo in self.biblioteca

    def favoritar_titulo(self, titulo: Titulo) -> None:
        if titulo not in self.favoritos:
            self.favoritos.append(titulo)

    def desfavoritar_titulo(self, titulo: Titulo) -> None:
        if titulo in self.favoritos:
            self.favoritos.remove(titulo)

    def publicar_proposta(
        self,
        titulos_requeridos: list[Titulo],
        titulos_propostos: list[Titulo],
    ) -> "Proposta":
        if not titulos_propostos or not titulos_requeridos:
            raise ValueError("Informe ao menos um título proposto e um requerido.")
        for titulo in titulos_propostos:
            if titulo not in self.biblioteca:
                raise ValueError(f"Você não possui o título {titulo.nome!r}.")
        return Proposta(
            anunciante=self,
            titulos_propostos=titulos_propostos,
            titulos_requeridos=titulos_requeridos,
            data_publicacao=datetime.now(),
        )

    def __repr__(self) -> str:
        return f"Usuario(nome={self.nome!r})"


class Proposta:
    def __init__(
        self,
        anunciante: Usuario,
        titulos_propostos: list[Titulo],
        titulos_requeridos: list[Titulo],
        data_publicacao: datetime
    ):
        self.anunciante = anunciante
        self.titulos_propostos = titulos_propostos
        self.titulos_requeridos = titulos_requeridos
        self.data_publicacao = data_publicacao
        self.interessados: list[Usuario] = []
        self.status = "aberta"
        
    def esta_aberta(self) -> bool:
        return self.status == "aberta"

    def demonstrar_interesse(self, usuario: Usuario) -> None:
        if not self.esta_aberta():
            raise ValueError("A proposta não está aberta.")
        if usuario is self.anunciante:
            raise ValueError("O anunciante não pode se interessar pela própria proposta.")
        if usuario not in self.interessados:
            self.interessados.append(usuario)

    def remover_interesse(self, usuario: Usuario) -> None:
        if usuario in self.interessados:
            self.interessados.remove(usuario)

    def fechar_proposta(self, interessado: Usuario) -> None:
        if not self.esta_aberta():
            raise ValueError("A proposta não está aberta.")
        if interessado not in self.interessados:
            raise ValueError("Usuário não demonstrou interesse nesta proposta.")
        self.__trocar_titulos(interessado)
        self.status = "fechada"

    def cancelar_proposta(self) -> None:
        if not self.esta_aberta():
            raise ValueError("A proposta não está aberta.")
        self.status = "cancelada"

    def __trocar_titulos(self, interessado: Usuario) -> None:
        for titulo in self.titulos_propostos:
            if titulo not in self.anunciante.biblioteca:
                raise ValueError(f"Anunciante não possui mais {titulo.nome!r}.")
        for titulo in self.titulos_requeridos:
            if titulo not in interessado.biblioteca:
                raise ValueError(f"Interessado não possui {titulo.nome!r}.")

        for titulo in self.titulos_propostos:
            self.anunciante.remover_titulo_biblioteca(titulo)
            interessado.adicionar_titulo_biblioteca(titulo)
        for titulo in self.titulos_requeridos:
            interessado.remover_titulo_biblioteca(titulo)
            self.anunciante.adicionar_titulo_biblioteca(titulo)

    def __repr__(self) -> str:
        return f"Proposta(anunciante={self.anunciante.nome!r}, status={self.status!r})"
