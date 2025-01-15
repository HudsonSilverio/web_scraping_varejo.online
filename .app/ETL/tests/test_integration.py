# poetry run python test_integration.py

import unittest
from extract import pag_produto
from transform import parse_page
from load import save_to_database, criando_conexao, configuracao_df

class TestUnitarios(unittest.TestCase):
    def test_pag_produto(self):
        """Testa se a função retorna um HTML válido."""
        html = pag_produto()
        self.assertTrue("<html" in html and "</html>" in html)

    def test_parse_page(self):
        """Testa se a função de transformação retorna os dados corretos."""
        sample_html = """<html>
            <span id="productTitle" class="a-size-large product-title-word-break">Produto Exemplo</span>
            <span class="a-price-whole">1.234</span>
            <span class="a-offscreen">R$ 1.999,00</span>
        </html>"""
        result = parse_page(sample_html)
        expected = {
            'nome_produto': 'ProdutoExemplo',
            'preco_atual': 1234.0,
            'preco_antigo': 1999.0,
            'timestamp': result['timestamp']  # Timestamp é dinâmico
        }
        self.assertEqual(result['nome_produto'], expected['nome_produto'])
        self.assertEqual(result['preco_atual'], expected['preco_atual'])
        self.assertEqual(result['preco_antigo'], expected['preco_antigo'])

    def test_database_connection(self):
        """Testa se a conexão com o banco é bem-sucedida."""
        conn = criando_conexao()
        self.assertIsNotNone(conn)
        conn.close()

    def test_table_creation(self):
        """Testa se a tabela é criada corretamente."""
        conn = criando_conexao()
        configuracao_df(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT to_regclass('tv.prices')")
        result = cursor.fetchone()
        self.assertEqual(result[0], 'tv.prices')
        conn.close()

if __name__ == "__main__":
    unittest.main()
