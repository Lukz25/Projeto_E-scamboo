import unittest
from datetime import date

from classes import Autor, Genero, Titulo, Usuario


class TestAutor(unittest.TestCase):
    def setUp(self):
        self.ana = Usuario("Ana", "ana@example.com", "11", "01000-000")
        self.machado = Autor(1, "Machado de Assis")
        self.dom = Titulo(1, "Dom Casmurro", self.ana, [], [], "1899", "bom", "")

    def test_adicionar_obra_liga_os_dois_lados(self):
        self.machado.adicionar_obra(self.dom)
        self.assertIn(self.dom, self.machado.obras)
        self.assertIn(self.machado, self.dom.autores)

    def test_adicionar_obra_repetida_nao_duplica(self):
        self.machado.adicionar_obra(self.dom)
        self.machado.adicionar_obra(self.dom)
        self.assertEqual(self.machado.obras, [self.dom])
        self.assertEqual(self.dom.autores, [self.machado])

    def test_remover_obra_desliga_os_dois_lados(self):
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

    def test_criar_titulo_coloca_na_biblioteca_do_dono(self):
        self.assertIs(self.iliada.usuario, self.ana)
        self.assertIn(self.iliada, self.ana.biblioteca)

    def test_criar_titulo_atualiza_obras_do_autor(self):
        self.assertEqual(self.homero.obras, [self.iliada])

    def test_data_lancamento_aceita_texto(self):
        self.assertEqual(self.iliada.data_lancamento, "VIII a.C.")

    def test_autores(self):
        gaiman = Autor(2, "Neil Gaiman")
        self.iliada.adicionar_autor(gaiman)
        self.assertTrue(self.iliada.possui_autor(gaiman))
        self.assertIn(self.iliada, gaiman.obras)
        self.iliada.remover_autor(gaiman)
        self.assertFalse(self.iliada.possui_autor(gaiman))
        self.assertNotIn(self.iliada, gaiman.obras)

    def test_generos(self):
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

    def test_email_invalido(self):
        with self.assertRaises(ValueError):
            Usuario("X", "sem-arroba", "11", "01000-000")
        with self.assertRaises(ValueError):
            self.ana.set_email("outro-sem-arroba")
        self.assertEqual(self.ana.get_email(), "ana@example.com")

    def test_set_email(self):
        self.ana.set_email("ana.souza@example.com")
        self.assertEqual(self.ana.get_email(), "ana.souza@example.com")

    def test_adicionar_titulo_repetido(self):
        with self.assertRaises(ValueError):
            self.ana.adicionar_titulo_biblioteca(self.dom)

    def test_remover_titulo(self):
        self.ana.favoritar_titulo(self.dom)
        self.ana.remover_titulo_biblioteca(self.dom)
        self.assertFalse(self.ana.possui_titulo(self.dom))
        self.assertNotIn(self.dom, self.ana.favoritos)

    def test_remover_titulo_que_nao_possui(self):
        with self.assertRaises(ValueError):
            self.ana.remover_titulo_biblioteca(self.bras)

    def test_favoritos(self):
        self.ana.favoritar_titulo(self.bras)
        self.ana.favoritar_titulo(self.bras)
        self.assertEqual(self.ana.favoritos, [self.bras])
        self.ana.desfavoritar_titulo(self.bras)
        self.assertEqual(self.ana.favoritos, [])

    def test_fazer_proposta(self):
        proposta = self.bia.fazer_proposta(self.dom, [self.bras], "Troca?")
        self.assertIs(proposta.interessado, self.bia)
        self.assertIs(proposta.titulo_desejado, self.dom)
        self.assertEqual(proposta.titulos_oferecidos, [self.bras])
        self.assertEqual(proposta.observacao, "Troca?")
        self.assertEqual(proposta.data_criacao, date.today())
        self.assertTrue(proposta.esta_pendente())

    def test_fazer_proposta_sem_oferecer_nada(self):
        with self.assertRaises(ValueError):
            self.bia.fazer_proposta(self.dom, [])

    def test_fazer_proposta_oferecendo_livro_de_outro(self):
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

    def test_aceitar_troca_os_donos(self):
        self.proposta.aceitar_proposta(self.ana)
        self.assertEqual(self.proposta.situacao, "aceita")
        self.assertIs(self.dom.usuario, self.bia)
        self.assertIs(self.bras.usuario, self.ana)
        self.assertIs(self.quincas.usuario, self.ana)
        self.assertEqual(self.ana.biblioteca, [self.bras, self.quincas])
        self.assertEqual(self.bia.biblioteca, [self.dom])

    def test_aceitar_tira_dos_favoritos_do_antigo_dono(self):
        self.ana.favoritar_titulo(self.dom)
        self.proposta.aceitar_proposta(self.ana)
        self.assertNotIn(self.dom, self.ana.favoritos)

    def test_so_o_dono_pode_aceitar(self):
        with self.assertRaises(ValueError):
            self.proposta.aceitar_proposta(self.caio)
        with self.assertRaises(ValueError):
            self.proposta.aceitar_proposta(self.bia)
        self.assertTrue(self.proposta.esta_pendente())

    def test_recusar(self):
        self.proposta.recusar_proposta(self.ana)
        self.assertEqual(self.proposta.situacao, "recusada")
        self.assertIs(self.dom.usuario, self.ana)
        self.assertIs(self.bras.usuario, self.bia)

    def test_so_o_dono_pode_recusar(self):
        with self.assertRaises(ValueError):
            self.proposta.recusar_proposta(self.caio)

    def test_cancelar(self):
        self.proposta.cancelar_proposta(self.bia)
        self.assertEqual(self.proposta.situacao, "cancelada")

    def test_so_o_interessado_pode_cancelar(self):
        with self.assertRaises(ValueError):
            self.proposta.cancelar_proposta(self.ana)

    def test_nao_responde_proposta_que_nao_esta_pendente(self):
        self.proposta.recusar_proposta(self.ana)
        with self.assertRaises(ValueError):
            self.proposta.aceitar_proposta(self.ana)
        with self.assertRaises(ValueError):
            self.proposta.recusar_proposta(self.ana)
        with self.assertRaises(ValueError):
            self.proposta.cancelar_proposta(self.bia)

    def test_aceitar_quando_interessado_nao_tem_mais_o_livro(self):
        self.bia.remover_titulo_biblioteca(self.bras)
        with self.assertRaises(ValueError):
            self.proposta.aceitar_proposta(self.ana)
        self.assertTrue(self.proposta.esta_pendente())
        self.assertIs(self.dom.usuario, self.ana)
        self.assertIn(self.quincas, self.bia.biblioteca)


if __name__ == "__main__":
    unittest.main()
