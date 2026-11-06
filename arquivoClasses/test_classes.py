import unittest
from datetime import date

from arquivoClasses import Autor, Genero, Titulo, Usuario

class TestAutor(unittest.TestCase):
    def setUp(self):
        self.ana = Usuario("Ana", "ana@example.com", "11", "01000-000")
        self.machado = Autor(1, "Machado de Assis")
        self.dom = Titulo(1, "Dom Casmurro", self.ana, [], [], "1899", "bom", "")

    def testAdicionarObra(self):
        self.machado.adicionar_obra(self.dom)
        self.assertIn(self.dom, self.machado.obras)
        self.assertIn(self.machado, self.dom.autores)

    def testAdicionarObraRepetida(self):
        self.machado.adicionar_obra(self.dom)
        self.machado.adicionar_obra(self.dom)
        self.assertEqual(self.machado.obras, [self.dom])
        self.assertEqual(self.dom.autores, [self.machado])

    def testRemoverObra(self):
        self.machado.adicionar_obra(self.dom)
        self.machado.remover_obra(self.dom)
        self.assertNotIn(self.dom, self.machado.obras)
        self.assertNotIn(self.machado, self.dom.autores)


class TestTitulo(unittest.TestCase):
    def setUp(self):
        self.ana = Usuario("Ana", "ana@example.com", "11", "01000-000")
        self.homero = Autor(1, "Homero")
        self.epico = Genero(1, "Épico")
        self.iliada = Titulo(1, "Ilíada", self.ana, [self.homero], [self.epico], "VIII a.C.", "novo", "")

    def testCriarTitulo(self):
        self.assertIs(self.iliada.usuario, self.ana)
        self.assertIn(self.iliada, self.ana.biblioteca)

    def testCriarTituloAtualizacao(self):
        self.assertEqual(self.homero.obras, [self.iliada])

    def testDataLancamentoAceitaTexto(self):
        self.assertEqual(self.iliada.data_lancamento, "VIII a.C.")

    def testAutores(self):
        gaiman = Autor(2, "Neil Gaiman")
        self.iliada.adicionar_autor(gaiman)
        self.assertTrue(self.iliada.possui_autor(gaiman))
        self.assertIn(self.iliada, gaiman.obras)
        self.iliada.remover_autor(gaiman)
        self.assertFalse(self.iliada.possui_autor(gaiman))
        self.assertNotIn(self.iliada, gaiman.obras)

    def testGeneros(self):
        fantasia = Genero(2, "Fantasia")
        self.iliada.adicionar_genero(fantasia)
        self.iliada.adicionar_genero(fantasia)
        self.assertEqual(self.iliada.generos, [self.epico, fantasia])
        self.iliada.remover_genero(fantasia)
        self.assertFalse(self.iliada.possui_genero(fantasia))
        self.assertTrue(self.iliada.possui_genero(self.epico))


class TestUsuario(unittest.TestCase):
    def setUp(self):
        self.ana = Usuario("Ana", "ana@example.com", "11", "01000-000")
        self.bia = Usuario("Bia", "bia@example.com", "12", "02000-000")
        self.dom = Titulo(1, "Dom Casmurro", self.ana, [], [], "1899", "bom", "")
        self.bras = Titulo(2, "Brás Cubas", self.bia, [], [], "1881", "ótimo", "")

    def testEmailInvalido(self):
        with self.assertRaises(ValueError):
            Usuario("X", "sem-arroba", "11", "01000-000")
        with self.assertRaises(ValueError):
            self.ana.set_email("outro-sem-arroba")
        self.assertEqual(self.ana.get_email(), "ana@example.com")

    def testSetEmail(self):
        self.ana.set_email("ana.souza@example.com")
        self.assertEqual(self.ana.get_email(), "ana.souza@example.com")

    def testAdicionarTituloRepetido(self):
        with self.assertRaises(ValueError):
            self.ana.adicionar_titulo_biblioteca(self.dom)

    def testRemoverTitulo(self):
        self.ana.favoritar_titulo(self.dom)
        self.ana.remover_titulo_biblioteca(self.dom)
        self.assertFalse(self.ana.possui_titulo(self.dom))
        self.assertNotIn(self.dom, self.ana.favoritos)

    def testRemoverTituloNaoPossui(self):
        with self.assertRaises(ValueError):
            self.ana.remover_titulo_biblioteca(self.bras)

    def testFavoritos(self):
        self.ana.favoritar_titulo(self.bras)
        self.ana.favoritar_titulo(self.bras)
        self.assertEqual(self.ana.favoritos, [self.bras])
        self.ana.desfavoritar_titulo(self.bras)
        self.assertEqual(self.ana.favoritos, [])

    def testFazerProposta(self):
        proposta = self.bia.fazer_proposta(self.dom, [self.bras], "Troca?")
        self.assertIs(proposta.interessado, self.bia)
        self.assertIs(proposta.titulo_desejado, self.dom)
        self.assertEqual(proposta.titulos_oferecidos, [self.bras])
        self.assertEqual(proposta.observacao, "Troca?")
        self.assertEqual(proposta.data_criacao, date.today())
        self.assertTrue(proposta.esta_pendente())

    def testFazerPropostaSemOferecerNada(self):
        with self.assertRaises(ValueError):
            self.bia.fazer_proposta(self.dom, [])

    def testFazerPropostaOferecendoLivroDeOutro(self):
        with self.assertRaises(ValueError):
            self.bia.fazer_proposta(self.dom, [self.dom])


class TestProposta(unittest.TestCase):
    def setUp(self):
        self.ana = Usuario("Ana", "ana@example.com", "11", "01000-000")
        self.bia = Usuario("Bia", "bia@example.com", "12", "02000-000")
        self.caio = Usuario("Caio", "caio@example.com", "13", "03000-000")
        self.dom = Titulo(1, "Dom Casmurro", self.ana, [], [], "1899", "bom", "")
        self.bras = Titulo(2, "Brás Cubas", self.bia, [], [], "1881", "ótimo", "")
        self.quincas = Titulo(3, "Quincas Borba", self.bia, [], [], "1891", "regular", "")
        self.proposta = self.bia.fazer_proposta(self.dom, [self.bras, self.quincas])

    def testAceitarTrocaDonos(self):
        self.proposta.aceitar_proposta(self.ana)
        self.assertEqual(self.proposta.situacao, "aceita")
        self.assertIs(self.dom.usuario, self.bia)
        self.assertIs(self.bras.usuario, self.ana)
        self.assertIs(self.quincas.usuario, self.ana)
        self.assertEqual(self.ana.biblioteca, [self.bras, self.quincas])
        self.assertEqual(self.bia.biblioteca, [self.dom])

    def testAceitarTirarFavoritosDoAntigoDono(self):
        self.ana.favoritar_titulo(self.dom)
        self.proposta.aceitar_proposta(self.ana)
        self.assertNotIn(self.dom, self.ana.favoritos)

    def testSoODonoPodeAceitar(self):
        with self.assertRaises(ValueError):
            self.proposta.aceitar_proposta(self.caio)
        with self.assertRaises(ValueError):
            self.proposta.aceitar_proposta(self.bia)
        self.assertTrue(self.proposta.esta_pendente())

    def testRecusar(self):
        self.proposta.recusar_proposta(self.ana)
        self.assertEqual(self.proposta.situacao, "recusada")
        self.assertIs(self.dom.usuario, self.ana)
        self.assertIs(self.bras.usuario, self.bia)

    def testSoODonoPodeRecusar(self):
        with self.assertRaises(ValueError):
            self.proposta.recusar_proposta(self.caio)

    def testCancelar(self):
        self.proposta.cancelar_proposta(self.bia)
        self.assertEqual(self.proposta.situacao, "cancelada")

    def testSoOInteressadoPodeCancelar(self):
        with self.assertRaises(ValueError):
            self.proposta.cancelar_proposta(self.ana)

    def testNaoRespondePropostaQueNaoEstaPendente(self):
        self.proposta.recusar_proposta(self.ana)
        with self.assertRaises(ValueError):
            self.proposta.aceitar_proposta(self.ana)
        with self.assertRaises(ValueError):
            self.proposta.recusar_proposta(self.ana)
        with self.assertRaises(ValueError):
            self.proposta.cancelar_proposta(self.bia)

    def testAceitarQuandoInteressadoNaoTemMaisLivro(self):
        self.bia.remover_titulo_biblioteca(self.bras)
        with self.assertRaises(ValueError):
            self.proposta.aceitar_proposta(self.ana)
        self.assertTrue(self.proposta.esta_pendente())
        self.assertIs(self.dom.usuario, self.ana)
        self.assertIn(self.quincas, self.bia.biblioteca)


if __name__ == "__main__":
    unittest.main()
