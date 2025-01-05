import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import pandas as pd
from extract import parse_page, pag_produto


def criando_conexao(db_name='tv_sansung_prices.db'):
    """Cria uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(db_name)
    return conn

def configuracao_df(conn):
    """Cria a tabela de preços se ela não existir."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            nome_produto INTEGER,
            preco_atual INTEGER,
            preco_antigo INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()

def save_to_database(conn, data):
    """Salva uma linha de dados no banco de dados SQLite usando pandas."""
    df = pd.DataFrame([data])  # Converte o dicionário em um DataFrame de uma linha
    df.to_sql('prices', conn, if_exists='append', index=False)  # Salva no banco de dados

# Teste das funções
if __name__ == '__main__':
    # Configuração do banco de dados
    conn = criando_conexao()
    configuracao_df(conn)

    while True:
        # Faz a requisição e parseia a página
        conteudo_pag = pag_produto()
        coleta = parse_page(conteudo_pag)
        
        # Salva os dados no banco de dados SQLite
        save_to_database(conn, coleta)
        print("Dados salvos no banco:", coleta)
        
        # Aguarda 10 segundos antes da próxima execução
        time.sleep(10)

    # Fecha a conexão com o banco de dados
    conn.close()