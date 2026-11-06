from arquivoClasses.classes import Autor, Genero, Proposta, Titulo, Usuario

usuarios: dict[str, Usuario] = {}
autores: dict[int, Autor] = {}
generos: dict[int, Genero] = {}
titulos: dict[int, Titulo] = {}
propostas: list[Proposta] = []


def carregar_dados_iniciais() -> None:
    usuarios.clear()
    autores.clear()
    generos.clear()
    titulos.clear()
    propostas.clear()

    ana = Usuario("Ana Souza", "ana@example.com", "(11) 90000-0001", "01001-000")
    bruno = Usuario("Bruno Lima", "bruno@example.com", "(11) 90000-0002", "04538-133")
    carla = Usuario("Carla Mendes", "carla@example.com", "(21) 90000-0003", "20040-020")
    diego = Usuario("Diego Rocha", "diego@example.com", "(31) 90000-0004", "30130-010")
    for usuario in [ana, bruno, carla, diego]:
        usuarios[usuario.get_email()] = usuario

    machado = Autor(1, "Machado de Assis")
    homero = Autor(2, "Homero")
    aluisio = Autor(3, "Aluísio Azevedo")
    gaiman = Autor(4, "Neil Gaiman")
    pratchett = Autor(5, "Terry Pratchett")
    orwell = Autor(6, "George Orwell")
    sun_tzu = Autor(7, "Sun Tzu")
    tolkien = Autor(8, "J. R. R. Tolkien")
    for autor in [machado, homero, aluisio, gaiman, pratchett, orwell, sun_tzu, tolkien]:
        autores[autor.id] = autor

    romance = Genero(1, "Romance")
    epico = Genero(2, "Épico")
    fantasia = Genero(3, "Fantasia")
    comedia = Genero(4, "Comédia")
    distopia = Genero(5, "Distopia")
    filosofia = Genero(6, "Filosofia")
    for genero in [romance, epico, fantasia, comedia, distopia, filosofia]:
        generos[genero.id] = genero

    lista_titulos = [
        Titulo(1, "Dom Casmurro", ana, [machado], [romance], "1899", "bom", "Edição de bolso."),
        Titulo(2, "Memórias Póstumas de Brás Cubas", bruno, [machado], [romance], "1881", "regular", "Algumas páginas grifadas."),
        Titulo(3, "Ilíada", carla, [homero], [epico], "VIII a.C.", "novo", "Tradução em versos."),
        Titulo(4, "Odisseia", ana, [homero], [epico], "VIII a.C.", "bom", ""),
        Titulo(5, "O Cortiço", diego, [aluisio], [romance], "1890", "desgastado", "Capa solta."),
        Titulo(6, "Belas Maldições", bruno, [gaiman, pratchett], [fantasia, comedia], "1990", "novo", ""),
        Titulo(7, "1984", carla, [orwell], [distopia], "1949", "bom", ""),
        Titulo(8, "A Arte da Guerra", diego, [sun_tzu], [filosofia], "V a.C.", "regular", ""),
        Titulo(9, "A Sociedade do Anel", ana, [tolkien], [fantasia], "1954", "novo", "Capa dura."),
    ]
    for titulo in lista_titulos:
        titulos[titulo.id] = titulo

    ana.favoritar_titulo(titulos[7])
    diego.favoritar_titulo(titulos[3])
    bruno.favoritar_titulo(titulos[9])

    propostas.append(bruno.fazer_proposta(titulos[1], [titulos[2]], "Troco o Brás Cubas pelo Dom Casmurro."))
    propostas.append(carla.fazer_proposta(titulos[8], [titulos[7]], "Topa trocar pelo 1984?"))


carregar_dados_iniciais()
