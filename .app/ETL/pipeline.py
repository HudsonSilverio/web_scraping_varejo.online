from .extract import parse_page, pag_produto
from .load import criando_conexao, configuracao_df,save_to_database, maximo_venda
from .transform import dataframe

def pipeline_completa(url, html, coleta, df, conn, data, db_name):