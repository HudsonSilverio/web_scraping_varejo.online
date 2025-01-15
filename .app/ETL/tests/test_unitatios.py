# poetry run python test_unitatios.py

import unittest
from extract import pag_produto
from transform import parse_page
from load import save_to_database, criando_conexao, configuracao_df

class TestIntegration(unittest.TestCase):
    def test_full_etl(self):
        """Testa o pipeline completo de extração, transformação e carregamento."""
        # Etapa de extração
        html = pag_produto()
        self.assertTrue("<html" in html and "</html>" in html)

        # Etapa de transformação
        data = parse_page(html)
        self.assertIn('nome_produto', data)
        self.assertIn('preco_atual', data)
        self.assertIn('preco_antigo', data)
        self.assertIn('timestamp', data)

        # Etapa de carregamento
        conn = criando_conexao()
        configuracao_df(conn)
        save_to_database(data)
        
        # Verifica se os dados foram salvos no banco
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tv.prices ORDER BY id DESC LIMIT 1;")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        conn.close()

if __name__ == "__main__":
    unittest.main()


